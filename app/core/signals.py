# DJANGO IMPORTS
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
# LOCAL IMPOTRS
from core.models import UserInfo, GroupInfo, GroupDependencyList
# MISC
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def global_user_add(sender, **kwargs):
    def call():
        user = kwargs.get('instance')
        if (kwargs.get('created')):
            logger.info("[SIGNAL] Creating UserInfo() for %s" % user)
            UserInfo(user=user).save()
    transaction.on_commit(call)

@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("[SIGNAL] Creating GroupInfo() for %s" % group)
        if (kwargs.get('created')):
            GroupInfo(group=group).save()
    transaction.on_commit(call)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change_discord_notify(sender, **kwargs):
    from modules.discord.tasks import send_discord_channel_message
    from modules.discord.models import DiscordChannel
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    group_pks = []
    for pk in kwargs.get('pk_set'):
        group_pks.append(pk)
    if action == "post_remove":
        for group in group_pks:
            group = Group.objects.get(pk=group)
            message = "You have been removed from the following group: **%s**." % group.name
            try:
                channel = DiscordChannel.objects.get(type="BOT").name
            except ObjectDoesNotExist:
                logger.warning("Please specify a BOT discord channel for Guild notifications.")
                return
            send_discord_channel_message.apply_async(
                args=[channel, message],
                kwargs={
                    'user': user.id
                }
            )
    elif action == "post_add":
        for group in group_pks:
            group = Group.objects.get(pk=group)
            message = "You have been added to the following group: **%s**." % group.name
            try:
                channel = DiscordChannel.objects.get(type="BOT").name
            except ObjectDoesNotExist:
                logger.warning("Please specify a BOT discord channel for Guild notifications.")
                return
            send_discord_channel_message.apply_async(
                args=[channel, message],
                kwargs={
                    'user': user.id
                }
            )

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change_check_dependent_groups(sender, **kwargs):
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    group_pks = []
    for pk in kwargs.get('pk_set'):
        logger.debug("Changed groups for user: %s" % group_pks)
        group_pks.append(pk)
    if action == "post_remove":
        for group in group_pks:
            logger.debug("Checking group %s for dependent groups" % group)
            group = Group.objects.get(pk=group)
            if (hasattr(group, 'dependency_list') and group.dependency_list.get_dependents()):
                logger.debug("Dependent groups for group: %s" % group.dependency_list.get_dependents())
                for dependent in group.dependency_list.get_dependents():
                    if dependent in user.groups.all():
                        logger.debug("Removing dependent group: %s" % dependent)
                        user.groups.remove(dependent)