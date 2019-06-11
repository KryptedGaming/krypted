from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DiscordConfig(AppConfig):
    name = 'modules.discord'

    # DISCORD SETTINGS
    DISCORD_API_ENDPOINT = "https://discordapp.com/api/v6"
    DISCORD_BASE_URI = 'https://discordapp.com/api/oauth2/authorize'
    DISCORD_TOKEN_URL = 'https://discordapp.com/api/oauth2/token'
    DISCORD_REVOKE_URL = 'https://discordapp.com/api/oauth2/token/revoke'
    DISCORD_CALLBACK_URL = settings.SERVER_DOMAIN + '/discord/callback'
    # USER SETTINGS
    DISCORD_SERVER_ID = '' # copy server id
    DISCORD_INVITE_LINK = 'https://discordapp.com/api/invites/{code}' # just replace the end code with the link
    DISCORD_CLIENT_ID = ''
    DISCORD_SECRET = ''
    DISCORD_BOT_TOKEN = ''

    def ready(self):
        pass
        from django.contrib.auth.models import User, Group
        from modules.discord.signals import user_group_change, global_group_add, global_group_remove
        m2m_changed.connect(user_group_change, sender=User.groups.through)
        pre_delete.connect(global_group_remove, sender=Group)
        post_save.connect(global_group_add, sender=Group)
