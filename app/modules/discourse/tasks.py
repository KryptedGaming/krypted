from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discourse.models import DiscourseGroup, DiscourseUser
from django.contrib.auth.models import Group, User
from django.conf import settings
import requests, json, logging
logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_discourse_group(self, group):
    group = Group.objects.get(pk=group)
    DiscourseGroup(group=group).save()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_discourse_group(self, group):
    DiscourseGroup(group__pk=group).delete()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_user_to_discourse_group(self, user, group):
    group = DiscourseGroup.objects.get(id=group)
    DiscourseUser.objects.get(auth_user__pk=user).add_group(group)

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_user_from_discourse_group(self, user, group):
    group = DiscourseGroup.objects.get(id=group)
    DiscourseUser.objects.get(auth_user__pk=user).remove_group(group)
