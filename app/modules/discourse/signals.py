from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from modules.discourse.tasks import *
from modules.discourse.models import *
import logging
logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    user = DiscourseUser.objects.get(auth_user=kwargs.get('instance'))
    action = str(kwargs.get('action'))
    groups = []
    logger.info("%s has changed with action %s" % (user, action))
    for pk in kwargs.get('pk_set'):
        logger.info("%s group added/removed" % pk)
        groups.append(DiscourseGroup.objects.get(group__pk=pk))
    if action == "post-remove":
        logger.info("removing")
        for group in groups:
            logger.info("Removing discourse user %s from discourse group %s" % (user, group))
            remove_user_from_discourse_group.apply_async(args=[user.user_id, group.role_id])
    elif action == "post_add":
        logger.info("adding")
        for group in groups:
            logger.info("Adding discourse user %s to discourse group %s" % (user, group))
            add_user_to_discourse_group.apply_async(args=[user.user_id, group.role_id])

@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    group = kwargs.get('instance')
    add_discourse_group.apply_async(args=[group.pk])

@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    group = DiscourseGroup.objects.get(group=kwargs.get('instance'))
    remove_discourse_group.apply_async(args=[group.role_id])
