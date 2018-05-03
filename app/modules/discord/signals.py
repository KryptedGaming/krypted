
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from modules.discord.models import *
from modules.discord.tasks import *
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    logger.info("[SIGNAL] Groups changed for user. Updating Discord groups.")
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    try:
        DiscordUser.objects.get(user=user)
        groups = []
        logger.info("[SIGNAL] %s groups have changed with action %s" % (user.username, action))
        for pk in kwargs.get('pk_set'):
            groups.append(DiscordGroup.objects.get(group__pk=pk))
        if action == "post_remove":
            for group in groups:
                logger.info("[SIGNAL] Removing %s from Discord Group %s" % (user.username, group))
                remove_user_from_discord_group.apply_async(args=[user.pk, group.id])
        elif action == "post_add":
            for group in groups:
                logger.info("[SIGNAL] Adding %s to Discord Group %s" % (user.username, group))
                add_user_to_discord_group.apply_async(args=[user.pk, group.id])
    except Exception as e:
        logger.info("[SIGNAL] Failed to updated Discord groups. %s" % e)


@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("[SIGNAL] Group change. Adding discord group %s" % group.name)
        add_discord_group.apply_async(args=[group.pk])
    transaction.on_commit(call)

@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    try:
        group = DiscordGroup.objects.get(group=kwargs.get('instance'))
        logger.info("[SIGNAL] Group change. Removing discord group %s" % group.group.name)
        remove_discord_group.apply_async(args=[group.group.pk])
    except Exception as e:
        logger.info("[SIGNAL] Could not remove Discord role. Roles may be out of sync. %s" % e)
