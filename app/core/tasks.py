from __future__ import absolute_import, unicode_literals
from celery import task
from django.contrib.auth.models import User, Group
from modules.discord.tasks import sync_discord_user
from app.conf import groups as group_settings
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def assign_community_groups():
    for user in User.objects.all():
        update_user_community_groups(user.pk)
@task()
def update_user_community_groups(user_id):
    user = User.objects.get(pk=user_id)
    if not user.discord:
        return None
    tenure = user.get_tenure()
    member = user.guilds.count() > 0
    recruit_group = Group.objects.get(name=group_settings.RECRUIT_GROUP)
    member_group = Group.objects.get(name=group_settings.MINOR_GROUP)
    veteran_group = Group.objects.get(name=group_settings.MAIN_GROUP)
    guest_group = Group.objects.get(name=group_settings.GUEST_GROUP)
    if member:
        if tenure < 0.3 and recruit_group not in user.groups.all():
            print("Adding %s to Recruit" % user)
            user.groups.add(recruit_group)
            if member_group in user.groups.all():
                user.groups.remove(member_group)
                time.sleep(1)
            if veteran_group in user.groups.all():
                user.groups.remove(veteran_group)
        elif tenure > 0.3 and tenure < 1.0 and member_group not in user.groups.all():
            print("Adding %s to Member" % user)
            user.groups.add(member_group)
            if recruit_group in user.groups.all():
                user.groups.remove(recruit_group)
                time.sleep(1)
            if veteran_group in user.groups.all():
                user.groups.remove(veteran_group)
        elif tenure > 1.0 and veteran_group not in user.groups.all():
            print("Adding %s to Veteran" % user)
            user.groups.add(veteran_group)
            time.sleep(1)
            if recruit_group in user.groups.all():
                user.groups.remove(recruit_group)
                time.sleep(1)
            if member_group in user.groups.all():
                user.groups.remove(member_group)
    else:
        if recruit_group in user.groups.all():
            user.groups.remove(recruit_group)
            time.sleep(1)
        if member_group in user.groups.all():
            user.groups.remove(member_group)
            time.sleep(1)

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
