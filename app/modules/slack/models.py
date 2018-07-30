from __future__ import absolute_import, unicode_literals
from django.db import models
from django.conf import settings
from core.models import User, Group, ModuleUser, ModuleGroup
from core.exceptions import RateLimitException
import requests, json, logging
logger = logging.getLogger(__name__)

# Create your models here.
class SlackUser(ModuleUser):
    groups = models.ManyToManyField("SlackGroup")
    def get_user(self):
        pass

    def add_group(self, slack_group):
        pass

    def remove_channel(self, channel):
        pass

class SlackGroup(ModuleGroup):
    """
    Technically, this is a slack channel
    However, we are going to treat slack channels as specific group channels, the only difference is that multiple groups point to it
    """
    groups = models.ManyToManyField(Group, null=True, blank=True)

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass
