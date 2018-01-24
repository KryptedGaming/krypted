from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discord.models import *
from django.contrib.auth.models import User, Group
from modules.discord.utils import *


@task()
def sync_groups():
    for group in Group.objects.all():
        if DiscordRole.objects.filter(group=group).count() == 0:
            addDiscordGroup(group)
    # TODO : add method to delete old Discord groups

@task()
def sync_users():
    for user in User.objects.all():
        syncUser(user)
