from django.db import models
from django.contrib.auth.models import User, Group
import logging
logger = logging.getLogger(__name__)

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
