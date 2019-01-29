# DJANGO IMPORTS
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
# INTERNAL IMPORTS
from modules.discourse.tasks import *
from modules.discourse.models import *
# MISC
import logging
logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    try:
        user = kwargs.get('instance')
        action = str(kwargs.get('action'))
        groups = []
        for pk in kwargs.get('pk_set'):
            groups.append(pk)
        if action == "post_remove":
            for group in groups:
                logger.info("[SIGNAL] Removing discourse user %s from discourse group %s" % (user, group))
                remove_user_from_discourse_group.apply_async(args=[user.id, group])
        elif action == "post_add":
            for group in groups:
                logger.info("[SIGNAL] Adding discourse user %s to discourse group %s" % (user, group))
                add_user_to_discourse_group.apply_async(args=[user.id, group])
    except Exception as e:
        logger.error("Failed to update user groups. %s" % e)


@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("[SIGNAL] Group %s added. Adding to Discourse." % group.name)
        add_discourse_group.apply_async(args=[group.pk])
    transaction.on_commit(call)


@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    try:
        group = kwargs.get('instance')
        discourse_group = DiscourseGroup.objects.get(group=group)
        logger.info("[SIGNAL] Group %s removed. Removing from Discourse." % group.name)
        remove_discourse_group.apply_async(args=[discourse_group.external_id])
    except:
        logger.error("[SIGNAL] Discourse Group was not found, groups may be out of sync.")
