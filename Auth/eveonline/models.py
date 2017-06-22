from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Token(models.Model):
    ## EVE CHARACTER
    character_id = models.IntegerField(blank=True, null=True)
    character_owner_hash = models.CharField(max_length=256)
    character_name = models.CharField(max_length=256)

    ## SSO
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=128)
    expires_on = models.DateTimeField(blank=True, null=True)

class MainCharacter(models.Model):
    character_name = models.CharField(max_length=256, primary_key=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class AlternateCharacter(models.Model):
    character_name = models.CharField(max_length=256, primary_key=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## LINK TO MAIN CHARACTER
    main = models.ManyToManyField("MainCharacter")
