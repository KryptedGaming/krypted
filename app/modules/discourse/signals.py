from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from modules.discourse.tasks import *
from modules.discourse.models import *
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    user = DiscourseUser.objects.get(auth_user=kwargs.get('instance'))
    action = str(kwargs.get('action'))
    groups = []
    for pk in kwargs.get('pk_set'):
        groups.append(DiscourseGroup.objects.get(group__pk=pk))
    if action == "post_remove":
        for group in groups:
            logger.info("[SIGNAL] Removing discourse user %s from discourse group %s" % (user, group))
            remove_user_from_discourse_group.apply_async(args=[user.user_id, group.role_id])
    elif action == "post_add":
        for group in groups:
            logger.info("[SIGNAL]Adding discourse user %s to discourse group %s" % (user, group))
            add_user_to_discourse_group.apply_async(args=[user.user_id, group.role_id])

@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("Group %s added. Adding to Discourse." % group.name)
        add_discourse_group.apply_async(args=[group.pk])
    transaction.on_commit(call)


@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    try:
        group = DiscourseGroup.objects.get(group=kwargs.get('instance'))
        logger.info("[SIGNAL] Group %s removed. Removing from Discourse." % group.group.name)
        remove_discourse_group.apply_async(args=[group.role_id])
    except:
        logger.error("[SIGNAL] Discourse Group was not found, groups may be out of sync.")
