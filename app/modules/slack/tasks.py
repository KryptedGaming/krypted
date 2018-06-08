from __future__ import absolute_import, unicode_literals
from celery import task
from django.contrib.auth.models import Group, User
from django.conf import settings
from modules.slack.models import *
import requests, json, logging
logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

@task()
def sync_slack_users():
    logger.info("Syncing slack users")
    for user in User.objects.all():
        try:
            slack_user = SlackUser.objects.get(user=user)
            logger.info("Retrieved slack user for %s" % user.pk)
        except Exception as e:
            slack_user = None
            logger.info("Searching for slack user %s: %s" % (user.pk, e))
            get_slack_user.apply_async(args=[user.pk])

        if slack_user:
            for group in slack_user.user.groups.all():
                if SlackChannel.objects.filter(groups__name__in=[group]).exists():
                    slack_channels = SlackChannel.objects.filter(groups__name__in=[group])
                    for slack_channel in slack_channels:
                        add_slack_user_to_channel.apply_async(args=[slack_channel.slack_id, slack_user.slack_id])

@task(bind=True)
def add_slack_user(self, user_pk):
    # Create slack user
    user = User.objects.get(pk=user_pk)
    SlackUser(user=user).save()

@task(bind=True)
def add_slack_channel(self, channel_name, groups=None):
    # Create slack channel
    SlackChannel(name=channel_name).save()
    # Get groups
    if groups:
        raw_groups = groups.split("-")
        groups = []
        for group in raw_groups:
            groups.append(Group.objects.get(pk=group))
    # Set channel groups
    SlackChannel.objects.get(name=channel_name).groups.set(groups)


@task(bind=True)
def add_slack_user_to_channel(self, channel_name, user_pk):
    slack_channel = SlackChannel.objects.get(name=channel_name)
    user = User.objects.get(pk=user_pk)
    SlackUser.objects.get(user=user).add_channel(slack_channel)

@task(bind=True)
def remove_slack_user_from_channel(self, channel_name, user_pk):
    slack_channel = SlackChannel.objects.get(name = channel_name)
    user = User.objects.get(pk=user_pk)
    SlackUser.objects.get(user=user).remove_channel(slack_channel)
