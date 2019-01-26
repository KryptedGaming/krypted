# DJANGO IMPORTS
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
from django.apps import apps
# INTERNAL IMPORTS
from modules.guilds.models import Guild, GuildApplication
# MISC
import logging

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=Guild.users.through)
def user_guild_change_notify_discord(sender, **kwargs):
    guild = kwargs.get('instance')
    action = str(kwargs.get('action'))
    user_ids = []
    for pk in kwargs.get('pk_set'):
        user_ids.append(pk)
    if action == "post_remove":
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            from modules.discord.tasks import send_discord_channel_message
            from modules.discord.models import DiscordChannel
            message = "You have been removed from the following guild: **%s**." % guild.name
            channel = DiscordChannel.objects.get(type="BOT").name
            send_discord_channel_message.apply_async(
            args=[channel, message],
            kwargs={
                'user': user.id
            }
            )

    elif action == "post_add":
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            from modules.discord.tasks import send_discord_channel_message
            from modules.discord.models import DiscordChannel
            message = "You have been added to the following guild: **%s**. You can now see guild groups in the Groups section." % guild.name
            channel = DiscordChannel.objects.get(type="BOT").name
            send_discord_channel_message.apply_async(
            args=[channel, message],
            kwargs={
                'user': user.id
            }
            )

@receiver(m2m_changed, sender=Guild.users_managing.through)
def user_guild_managing_change_notify_discord(sender, **kwargs):
    guild = kwargs.get('instance')
    action = str(kwargs.get('action'))
    user_ids = []
    for pk in kwargs.get('pk_set'):
        user_ids.append(pk)
    if action == "post_remove":
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            from modules.discord.tasks import send_discord_channel_message
            from modules.discord.models import DiscordChannel
            message = "You have been removed from the staff list for the following guild: **%s**" % guild.name
            channel = DiscordChannel.objects.get(type="BOT").name
            send_discord_channel_message.apply_async(
            args=[channel, message],
            kwargs={
                'user': user.id
            }
            )

    elif action == "post_add":
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            from modules.discord.tasks import send_discord_channel_message
            from modules.discord.models import DiscordChannel
            message = "You have been added to the staff list for the following guild: **%s**" % guild.name
            channel = DiscordChannel.objects.get(type="BOT").name
            send_discord_channel_message.apply_async(
            args=[channel, message],
            kwargs={
                'user': user.id
            }
            )
