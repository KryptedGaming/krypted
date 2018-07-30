from django.db import models
from django.conf import settings
from core.models import User, Group, ModuleUser, ModuleGroup
from core.exceptions import RateLimitException
import logging, requests, json
logger = logging.getLogger(__name__)

class DiscordUser(ModuleUser):
    # BASIC INFORMATION
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    # AUTHENTICATION
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    # REFERENCES
    groups = models.ManyToManyField("DiscordGroup")

    def add_group(self, discord_group):
        pass
    def remove_group(self, discord_group):
        pass

class DiscordGroup(ModuleGroup):
    # REFERENCES
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass 
