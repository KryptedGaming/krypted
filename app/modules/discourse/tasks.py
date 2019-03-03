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
    user = User.objects.get(pk=user_id)
    discourse_user = DiscourseUser.objects.get(user=user)
    logger.info("[DISCOURSE] Syncing groups for %s" % user.username)
    for discourse_group in discourse_user.groups.all():
        if discourse_group.group not in user.groups.all():
            logger.warning("[DISCOURSE] Found incorrect group %s for %s" % (discourse_group.group.name, user.username))
            remove_user_from_discourse_group.apply_async(args=[user_id, discourse_group.group.pk])

@task(bind=True, rate_limit="60/m")
def update_external_id(self, user_id):
    # pull objects from database
    discourse_user = DiscourseUser.objects.get(user__id=user_id)
    # call discourse client api
    response = DiscourseClient.get_discourse_user(discourse_user.user.username)
    # handle response
    if response.status_code == 429:
        logger.warning("[DISCOURSE] [RATELIMIT] Updating external ID for %s" % discourse_user.user.username)
        self.apply_async(args=[user_id], countdown=30)
    elif response.status_code == 200:
        logger.info("[DISCOURSE] [SUCCESS] Updating external ID for %s" % discourse_user.user.username)
        discourse_user.external_id = response.json()['user']['id']
        discourse_user.save()
    else:
        logger.error("[DISCOURSE] [ERROR] Updating external ID for %s" % discourse_user.user.username)
        logger.error("[DISCOURSE] [ERROR] Response: %s" % response.json())

@task(bind=True, rate_limit="60/m")
def add_discourse_group(self, group_id):
    # pull objects from database
    group = Group.objects.get(pk=group_id)
    # Check if exists
    if DiscourseGroup.objects.filter(group=group).exists():
        logger.warning("[DISCOURSE] Group already exists" % group.name)
        return True
    # call discourse client api
    response = DiscourseClient.add_group_to_discourse_server(group.name)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("[DISCOURSE] [RATELIMIT] Adding group [%s] to discourse forum" % group.name)
            self.apply_async(args=[group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("[DISCOURSE] [SUCCESS] Adding group %s to discourse forum" % group.name)
            discourse_group = DiscourseGroup(
                external_id=response.json()['basic_group']['id'],
                group=group
            )
            discourse_group.save()
        else:
            logger.error("[DISCOURSE] [ERROR] Adding Group %s to discourse forum" % group.name)
            logger.error("[DISCOURSE] [ERROR] Response: %s" % response.json())
        pass
    except Exception as e:
        logger.error("[DISCOURSE] [FATAL] Error with add_discourse_group function. %s" % e)

@task(bind=True, rate_limit="60/m")
def remove_discourse_group(self, discourse_group_external_id):
    discourse_group = DiscourseGroup.objects.get(external_id=discourse_group_external_id)
    # call discourse client api
    response = DiscourseClient.remove_group_from_discourse_server(discourse_group_external_id)
    # handle response
    try:
        if response.status_code == 429:
            logger.warning("[DISCOURSE] [RATELIMIT] - Removing Group [%s] from discourse forum" % discourse_group_external_id)
            self.apply_async(args=[discourse_group_external_id], countdown=60)
        elif response.status_code == 200:
            logger.info("[DISCOURSE] [SUCCESS] - Removing Group %s from discourse forum" % discourse_group_external_id)
            discourse_group.delete()
        else:
            logger.error("[DISCOURSE] [ERROR] Removing Group %s from discourse forum" % discourse_group_external_id)
            logger.error("[DISCOURSE] [ERROR] Response: %s" % response.json())
    except Exception as e:
        logger.error("[DISCOURSE] [FATAL] Error with remove_discourse_group function. %s" % e)


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
            logger.warning("[DISCOURSE] [RATELIMIT] Adding Discourse group %s to user %s" % (discourse_group, discourse_user))
            self.apply_async(args=[user_id, group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("[DISCOURSE] [SUCCESS] Adding Discourse group %s to user %s" % (discourse_group, discourse_user))
            discourse_user.groups.add(discourse_group)
        else:
            if "already a member" in response.json()['errors']:
                logger.warning("[DISCOURSE] [ALREADY_A_MEMBER] Adding Discourse group %s to user %s" % (discourse_group, discourse_user))
                pass
            logger.error("[DISCOURSE] [ERROR] Adding Discourse group %s to user %s" % (discourse_group, discourse_user))
            logger.error("[DISCOURSE] [ERROR] Response: %s" % response.json())
    except Exception as e:
        logger.error("[DISCOURSE] [FATAL] Error with add_user_to_discourse_group function. %s" % e)


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
            logger.warning("[DISCOURSE] [RATELIMIT] Removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
            self.apply_async(args=[user_id, group_id], countdown=60)
        elif response.status_code == 200:
            logger.info("[DISCOURSE] [SUCCESS] Removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
            discourse_user.groups.remove(discourse_group)
        else:
            logger.error("[DISCOURSE] [FAILURE] Removing Discourse group [%s] from user [%s]" % (discourse_group, discourse_user))
            logger.error("[DISCOURSE] [FAILURE] Response: %s" % response.json())
    except Exception as e:
        logger.error("[DISCOURSE] [FATAL] Error with remove_user_from_discourse_group function. %s" % e)
