from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.apps import apps
# INTERNAL IMPORTS
from modules.guilds.models import Guild
# MISC
import logging, time

logger = logging.getLogger(__name__)

@task()
def remove_user_from_guild(user_id, guild_id):
    user = User.objects.get(pk=user_id)
    guild = Guild.objects.get(pk=guild_id)

    if guild in user.guilds_in.all():
        guild.users.remove(user)
    for group in guild.groups.all():
        if group in user.groups.all():
            user.groups.remove(group)
