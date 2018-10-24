from __future__ import absolute_import, unicode_literals
from celery import task
from core.models import User, Group
from modules.discourse.models import DiscourseUser, DiscourseGroup
from modules.discord.models import DiscordUser, DiscordGroup
# from modules.discourse.tasks import sync_discourse_user
from modules.discord.tasks import sync_discord_user
from django.conf import settings
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def sync_user(user_id):
    # SYNC SERVICES
    logger.info("Syncing API roles for user %s" % user_id)
    call_counter = 0
    sync_discourse_user.apply_async(args=[user_id], countdown=call_counter)
    sync_discord_user.apply_async(args=[user_id], countdown=call_counter)
    call_counter += 1
    # SYNC COMMUNITY GROUPS
    logger.info("Syncing community roles for user %s" % user_id)
    user = User.objects.get(pk=user_id)
    call_counter = 0
    logger.info("User %s synced." % user_id)

@task()
def sync_all_users():
    call_counter = 1
    for user in User.objects.all():
        sync_user.apply_async(args=[user.id], countdown=call_counter*10)
        call_counter += 1

@task()
def hard_sync_user(user_id):
    user = User.objects.get(id=user_id)
    groups = []
    for group in user.groups.all():
        groups.append(group)
    for group in user.groups.all():
        time.sleep(1)
        user.groups.remove(group)
    for group in groups:
        time.sleep(1)
        user.groups.add(group)
