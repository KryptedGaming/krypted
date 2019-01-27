# DJANGO IMPORTS
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
# INTERNAL IMPORTS
from modules.discord.models import *
from modules.discord.tasks import *
# MISC
import logging

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    try:
        groups = []
        for pk in kwargs.get('pk_set'):
            groups.append(pk)
        if action == "post_remove":
            for group in groups:
                logger.info("[SIGNAL] Removing %s from group %s" % (user, group))
                remove_user_from_discord_group.apply_async(args=[user.pk, group])
        elif action == "post_add":
            for group in groups:
                logger.info("[SIGNAL] Adding %s to group %s" % (user, group))
                add_user_to_discord_group.apply_async(args=[user.pk, group])
    except Exception as e:
        logger.error("[SIGNAL] Failed to updated Discord groups. %s" % e)


@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("[SIGNAL] Adding group %s" % group)
        add_discord_group.apply_async(args=[group.pk])
    transaction.on_commit(call)

@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    try:
        discord_group = DiscordGroup.objects.get(group__pk=kwargs.get('instance').pk)
        logger.info("[SIGNAL] Removing group %s" % discord_group)
        remove_discord_group.apply_async(args=[discord_group.external_id])
    except Exception as e:
        logger.error("[SIGNAL] Could not remove Discord role. Roles may be out of sync. %s" % e)
