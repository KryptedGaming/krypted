from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discourse.utils import *
from modules.discourse.models import DiscourseGroup
from django.contrib.auth.models import User


@task()
def sync_groups():
    updateGroups()

@task()
def sync_users():
    updateGroups()
    for user in User.objects.all():
        # remove them from all the current groups
        # TODO : optimize so that it's just removing old ones. requires discourse group tracking
        for group in DiscourseGroup.objects.all():
            removeUserFromGroup(user, group)

        for group in user.groups.all():
            print(user.groups.all())
            try:
                addUserToGroup(user, DiscourseGroup.objects.get(group=group))
            except:
                pass
