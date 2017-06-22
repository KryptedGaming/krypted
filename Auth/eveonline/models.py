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
    expires_in = models.IntegerField(default=0)

    ## User
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.character_name

    def populate(self):
        data = {}
        data['access_token'] = self.access_token
        data['refresh_token'] = self.refresh_token
        data['expires_in'] = self.expires_in

        return data


class EveCharacter(models.Model):
    character_name = models.CharField(max_length=256, primary_key=True)
    character_portrait = models.URLField(max_length=256, blank=True, null=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ManyToManyField("EveCharacter", blank=True, null=True)

    def __str__(self):
        return self.character_name
