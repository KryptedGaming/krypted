from __future__ import absolute_import, unicode_literals
from celery import task
from django.contrib.auth.models import User, Group
from django.apps import apps
from modules.discord.tasks import sync_discord_user
import logging, time

logger = logging.getLogger(__name__)
core_settings = apps.get_app_config('core')

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def clear_inactive_users():
    for user in User.objects.all():
        if not user.info.discord or not user.info.discourse:
            clear_inactive_user.apply_async(args=[user.id])

@task()
def clear_inactive_user(user_id):
    user = User.objects.get(id=user_id)
    for group in user.groups.all():
        user.groups.remove(group)
    for guild in user.guilds_in.all():
        guild.users.remove(user)

@task()
def update_users_region_groups():
    for user in User.objects.all():
            update_user_region_groups.apply_async(args=[user.id])
@task()
def update_user_region_groups(user_id):
    user = User.objects.get(id=user_id)
    groups = []
    for region in core_settings.REGIONS:
        groups.append(Group.objects.get(name=region[0]))
    for group in groups:
        if group in user.groups.all() and group.name != user.info.region:
            user.groups.remove(group)
        if group not in user.groups.all() and group.name == user.info.region:
            user.groups.add(group)
