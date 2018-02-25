
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
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    groups = []
    logger.info("%s groups have changed with action %s" % (user.username, action))
    for pk in kwargs.get('pk_set'):
        groups.append(DiscordRole.objects.get(group__pk=pk))
    if action == "post_remove":
        for group in groups:
            logger.info("Removing %s from Discord Group %s" % (user.username, group))
            remove_user_from_discord_group.apply_async(args=[user.pk, group.role_id])
    elif action == "post_add":
        for group in groups:
            logger.info("Adding %s to Discord Group %s" % (user.username, group))
            add_user_to_discord_group.apply_async(args=[user.pk, group.role_id])

@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("Group change. Adding discord group %s" % group.name)
        add_discord_group.apply_async(args=[group.pk])
    transaction.on_commit(call)

@receiver(pre_delete, sender=Group)
def global_group_remove(sender, **kwargs):
    try:
        group = DiscordRole.objects.get(group=kwargs.get('instance'))
        logger.info("Group change. Removing discord group %s" % group.name)
        remove_discord_group.apply_async(args=[group.group.pk])
    except:
        logger.info("Could not remove Discord role. Roles may be out of sync.")
