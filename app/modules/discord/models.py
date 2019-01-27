from django.db import models
from django.contrib.auth.models import User, Group
from django.apps import apps
import logging
logger = logging.getLogger(__name__)
discord_settings = apps.get_app_config('discord')

class DiscordUser(models.Model):
    # BASIC INFORMATION
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    # AUTHENTICATION
    external_id = models.BigIntegerField(blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    # REFERENCES
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="discord_user")
    groups = models.ManyToManyField("DiscordGroup")

    def __str__(self):
        return self.username

class DiscordGroup(models.Model):
    external_id = models.BigIntegerField(blank=True, null=True)
    group = models.OneToOneField(Group, null=True, on_delete=models.SET_NULL, related_name="discord_group")

    def __str__(self):
        if self.group:
            return self.group.name
        else:
            return "None"

class DiscordChannel(models.Model):
    supported_channel_types = (
        ("BOT", "BOT"),
        ("HR", "HR"),
    )

    name = models.CharField(max_length=64)
    type = models.CharField(max_length=32, choices=supported_channel_types)
    external_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
