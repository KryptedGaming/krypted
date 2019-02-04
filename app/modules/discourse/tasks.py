from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS
from django.contrib.auth.models import Group
# LOCAL IMPORTS
from modules.discourse.models import DiscourseGroup, DiscourseUser
from modules.discourse.client import DiscourseClient
# MISC
import logging
logger = logging.getLogger(__name__)

@task()
def sync_discourse_user(user_id):
    pass

@task(bind=True, rate_limit="60/m")
def update_external_id(self, user_id):
    # pull objects from database
    discourse_user = DiscourseUser.objects.get(user__id=user_id)
    # call discourse client api
    response = DiscourseClient.get_discourse_user(discourse_user.user.username)
    # handle response
    if response.status_code == 429:
        logger.warning("RATELIMIT - Updating USERID for [%s]" % discourse_user.user.username)
        self.apply_async(args=[user_id], countdown=30)
    elif response.status_code == 200:
        logger.info("SUCCESS - Updating USERID for [%s]" % discourse_user.user.username)
        discourse_user.external_id = response.json()['user']['id']
        discourse_user.save()
    else:
        logger.error("FAILURE - Updating USERID for [%s]" % discourse_user.user.username)

@task(bind=True, rate_limit="60/m")
def add_discourse_group(self, group_id):
    # pull objects from database
    group = Group.objects.get(pk=group_id)
    # Check if exists
    if DiscourseGroup.objects.filter(group=group).exists():
        return True
    # call discourse client api
    response = DiscourseClient.add_group_to_discourse_server(group.name)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("RATELIMIT - Adding Group [%s] to Discourse Server." % group.name)
            self.apply_async(args=[group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("SUCCESS - Adding Group [%s] to Discourse Server." % group.name)
            discourse_group = DiscourseGroup(
                external_id=response.json()['basic_group']['id'],
                group=group
            )
            discourse_group.save()
        else:
            logger.error("FAILURE - Adding Group [%s] to Discourse Server. %s" % (group.name, response.json()))
        pass
    except Exception as e:
        logger.error("FATAL - Error with add_discourse_group function. %s" % e)

@task(bind=True, rate_limit="60/m")
def remove_discourse_group(self, discourse_group_external_id):
    discourse_group = DiscourseGroup.objects.get(external_id=discourse_group_external_id)
    # call discourse client api
    response = DiscourseClient.remove_group_from_discourse_server(discourse_group_external_id)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("RATELIMIT - Removing Group [%s] from Discourse Server." % discourse_group_external_id)
            self.apply_async(args=[discourse_group_external_id], countdown=60)
        elif response.status_code == 200:
            logger.info("SUCCESS - Removing Group [%s] from Discourse Server." % discourse_group_external_id)
            discourse_group.delete()
        else:
            logger.info("FAILURE - Removing Group [%s] from Discourse Server. %s" % (discourse_group_external_id, response.json()))
    except Exception as e:
        logger.error("FATAL - Error with remove_discourse_group function. %s" % e)


@task(bind=True, rate_limit="60/m")
def add_user_to_discourse_group(self, user_id, group_id):
    # pull objects from database
    discourse_user = DiscourseUser.objects.get(user__id=user_id)
    discourse_group = DiscourseGroup.objects.get(group__id=group_id)
    # check id
    if not discourse_user.external_id:
        update_external_id(discourse_user.user.id)
    # call discourse client api
    response = DiscourseClient.add_group_to_discourse_user(discourse_user.user.username, discourse_group.external_id)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("Rate limit adding Discourse group [%s] to user [%s]" % (discourse_group, discourse_user))
            self.apply_async(args=[user_id, group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("Success adding Discourse group [%s] to user [%s]" % (discourse_group, discourse_user))
            discourse_user.groups.add(discourse_group)
        else:
            if "already a member" in response.json()['errors']:
                pass
            logger.error("Error adding Discourse group [%s] to user [%s]" % (discourse_group, discourse_user, response.json()))
    except Exception as e:
        logger.error("FATAL - Error with add_user_to_discourse_group function. %s" % e)


@task(bind=True, rate_limit="60/m")
def remove_user_from_discourse_group(self, user_id, group_id):
    # pull objects from database
    discourse_user = DiscourseUser.objects.get(user__id=user_id)
    discourse_group = DiscourseGroup.objects.get(group__id=group_id)
    # check id
    if not discourse_user.external_id:
        update_external_id(discourse_user.user.id)
    # call discourse client api
    response = DiscourseClient.remove_group_from_discourse_user(discourse_user.external_id, discourse_group.external_id)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("Rate limit removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
            self.apply_async(args=[user_id, group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("Success removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
            discourse_user.groups.remove(discourse_group)
        else:
            logger.error("Failure removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
    except Exception as e:
        logger.error("FATAL - Error with remove_user_from_discourse_group function. %s" % e)
