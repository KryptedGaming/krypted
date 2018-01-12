from django.db import models
from django.contrib.auth.models import User, Group

class DiscordToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class DiscordRole(models.Model):
    role_id = models.CharField(max_length=255, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
