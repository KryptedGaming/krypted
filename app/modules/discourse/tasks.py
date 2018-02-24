from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discourse.models import DiscourseGroup, DiscourseUser
from django.contrib.auth.models import Group, User
from django.conf import settings
import requests, json, logging
logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

@task(bind=True, max_retries=None)
def add_discourse_group(self, group):
    try:
        api_add_group(group)
    except RateLimitException as e:
        pass
        # self.retry(exc=e, countdown=60)

@task(bind=True, max_retries=None)
def remove_discourse_group(self, group):
    try:
        api_remove_group(group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)

@task(bind=True, max_retries=None)
def add_user_to_discourse_group(self, user, group):
    try:
        api_add_user_to_group(user, group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)

@task(bind=True, max_retries=None)
def remove_user_from_discourse_group(self, user, group):
    try:
        api_remove_user_from_group(user, group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)


# Helpers
def api_add_group(group):
    """
    Expects a Standard Group object.
    """
    group = Group.objects.get(pk=group)
    url = settings.DISCOURSE_BASE_URL + "/admin/groups"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'group[name]': group.name
    }
    response = requests.post(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        response = dict(response.json())
        discourse_group = DiscourseGroup(role_id=response['basic_group']['id'], group=group)
        discourse_group.save()
def api_remove_group(group):
    """
    Expects a DiscourseGroup object.
    """
    group = DiscourseGroup.objects.get(role_id=group)
    logger.info("Removing Discourse group %s" % group)
    url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + str(group.role_id)
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
    }
    response = requests.delete(url=url, data=data)
    logger.info(response.status_code)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        logger.info("Successfully removed")
        group.delete()
    else:
        logger.info("Failed with %s" % response.json())
def api_remove_user_from_group(user, group):
    """
    Expects a Discourse User
    """
    group = DiscourseGroup.objects.get(role_id=group)
    user = DiscourseUser.objects.get(user_id=user)
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'usernames': user.auth_user.username.replace(" ", "_")
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        user.groups.add(group)
        logger.info("Added %s to %s" % (user.auth_user.username, group.group.name))
def api_add_user_to_group(user, group):
    group = DiscourseGroup.objects.get(role_id=group)
    user = DiscourseUser.objects.get(user_id=user)
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'user_id': user.user_id
    }
    response = requests.delete(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        user.groups.remove(group)
        logger.info("Removed %s from %s" % (user.auth_user.username, group.group.name))
