from django.db import models
from django.conf import settings
from core.models import User, Group, ModuleUser, ModuleGroup
from core.exceptions import RateLimitException
from modules.discord.client import DiscordClient
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

class DiscordGroup(ModuleGroup):
    def get_users():
        pass
