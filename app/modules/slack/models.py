from __future__ import absolute_import, unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.exceptions import RateLimitException
import requests, json, logging
logger = logging.getLogger(__name__)

# Create your models here.
class SlackUser(models.Model):
    slack_id = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    channels = models.ManyToManyField("SlackChannel")

    def save(self, *args, **kwargs):
        url = settings.SLACK_BASE_URL + "users.admin.invite"
        data = {
                'token': settings.SLACK_LEGACY_TOKEN,
                'email': self.user.email
        }
        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            if 'error' in response.json():
                if response.json()['error'] == 'already_in_team':
                    self.get_user()
                    super(SlackUser, self).save(*args, **kwargs)
            else:
                super(SlackUser, self).save(*args, **kwargs)

    def get_user(self):
        url = settings.SLACK_BASE_URL + "users.lookupByEmail"
        data = {
                'token': settings.SLACK_TOKEN,
                'email': self.user.email
        }

        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException

        elif response.status_code == 200:
            self.slack_id=response.json()['user']['id']

    def add_channel(self, channel):
        """
        Add a slack user to slack channel.
        Expects a SlackChannel() object.
        """
        if channel.groups.all():
            url = settings.SLACK_BASE_URL + "groups.invite"
        else:
            url = settings.SLACK_BASE_URL + "channels.invite"
        data = {
                'token': settings.SLACK_TOKEN,
                'channel': channel.slack_id,
                'user': self.slack_id
        }
        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.add(channel)

    def remove_channel(self, channel):
        """
        Remove a slack user from a slack channel.
        Expects a SlackChannel() object.
        """
        if channel.groups.all():
            url = settings.SLACK_BASE_URL + "groups.kick"
        else:
            url = settings.SLACK_BASE_URL + "channels.kick"
        data = {
                'token': settings.SLACK_TOKEN,
                'channel': channel.slack_id,
                'user': self.slack_id
        }
        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.remove(channel)

class SlackChannel(models.Model):
    name = models.CharField(max_length=32)
    slack_id = models.CharField(max_length=32, null=True, blank=True)
    groups = models.ManyToManyField(Group, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Create a Slack channel.
        Expects that you have set self.name and self.groups before saving.
        """
        url = settings.SLACK_BASE_URL + "groups.create"
        data = {
                'token': settings.SLACK_TOKEN,
                'name': self.name
        }

        response = requests.put(url=url, data=data)

        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.slack_id = str(dict(response.json())['group']['id'])
            super(SlackChannel, self).save(*args, **kwargs)
