from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discourse.models import DiscourseGroup, DiscourseUser
from django.contrib.auth.models import Group, User
from django.conf import settings
from core.exceptions import RateLimitException
import requests, json, logging
logger = logging.getLogger(__name__)

@task()
def sync_discourse_user(user_id):
    user = User.objects.get(id=user_id)
    try:
        discourse_user = DiscourseUser.objects.get(auth_user=user)
        call_counter = 0
        for discourse_group in DiscourseGroup.objects.all():
            if discourse_group.group in user.groups.all() and discourse_group not in discourse_user.groups.all():
                logger.info("%s has group %s (%s), but was missing it. Syncing." % (user.username, discourse_group.group.name, discourse_group.id))
                add_user_to_discourse_group.apply_async(args=[user.id, discourse_group.id], countdown=call_counter)
                call_counter += 1
            if discourse_group.group not in user.groups.all() and discourse_group in discourse_user.groups.all():
                logger.info("%s does not have group %s, but had it. Syncing." % (user.username, discourse_group.group.name))
                remove_user_from_discourse_group.apply_async(args=[user.id, discourse_group.id], countdown=call_counter)
                call_counter += 1
    except Exception as e:
        logger.info("Failed to sync Discourse user for %s. %s" % (user.username, e))

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_discourse_group(self, group):
    group = Group.objects.get(pk=group)
    DiscourseGroup(group=group).save()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_discourse_group(self, group):
    group = DiscourseGroup.objects.get(group__pk=group)
    group.delete()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_user_to_discourse_group(self, user, group):
    group = DiscourseGroup.objects.get(id=group)
    DiscourseUser.objects.get(auth_user__pk=user).add_group(group)

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_user_from_discourse_group(self, user, group):
    group = DiscourseGroup.objects.get(id=group)
    DiscourseUser.objects.get(auth_user__pk=user).remove_group(group)
