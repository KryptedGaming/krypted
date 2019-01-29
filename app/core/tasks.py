from __future__ import absolute_import, unicode_literals
from celery import task
from django.contrib.auth.models import User, Group
from modules.discord.tasks import sync_discord_user
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def clear_inactive_users():
    for user in User.objects.all():
        if not user.info.discord or not user.info.discourse:
            clear_inactive_user.apply_async(args=[user.id], countdown=call_counter*2)

@task()
def clear_inactive_user(user_id):
    user = User.objects.get(id=user_id)
    for group in user.groups.all():
        user.groups.remove(group)
    for guild in user.guilds_in.all():
        guild.users.remove(user)
