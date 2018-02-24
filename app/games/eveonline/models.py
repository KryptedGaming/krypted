from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
import datetime
from django.utils import timezone

# Create your models here.
class Token(models.Model):
    ## EVE CHARACTER
    character_id = models.IntegerField(blank=True, null=True)
    character_owner_hash = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255)


    ## SSO
    access_token = models.CharField(max_length=255)
    refresh_token = models.TextField(blank=True, null=True)
    expires_in = models.IntegerField(default=0)
    expiry = models.DateTimeField(blank=True, null=False, auto_now_add=True)

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

    def refresh(self):
        if timezone.now() > self.expiry:
            try:
                settings.ESI_SECURITY.update_token(self.populate())
                new_token = settings.ESI_SECURITY.refresh()
                self.access_token = new_token['access_token']
                self.refresh_token = new_token['refresh_token']
                self.expiry = timezone.now() + datetime.timedelta(0, new_token['expires_in'])
                self.save()
            except:
                self.delete()
        else:
            print("Token refresh not needed.")

    def force_refresh(self):
        try:
            settings.ESI_SECURITY.update_token(self.populate())
            new_token = settings.ESI_SECURITY.refresh()
            self.access_token = new_token['access_token']
            self.refresh_token = new_token['refresh_token']
            self.expiry = timezone.now() + datetime.timedelta(0, new_token['expires_in'])
            self.save()
            return True
        except:
            self.delete()
            return False

class EveCharacter(models.Model):
    character_name = models.CharField(max_length=255, primary_key=True)
    character_portrait = models.URLField(max_length=255, blank=True, null=True)
    character_alt_type = models.CharField(max_length=255, choices=settings.EVE_ALT_TYPES, null=True)
    character_corporation = models.CharField(max_length=255, blank=True, null=True)
    character_alliance = models.CharField(max_length=255, blank=True, null=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.character_name

    def update_corporation(self):
        try:
            self.token.refresh()
            esi_app = settings.ESI_APP
            esi_security = settings.ESI_SECURITY
            esi_security.update_token(self.token.populate())
            op = esi_app.op['get_characters_character_id'](character_id=self.token.character_id)
            corporation = settings.ESI_CLIENT.request(op)
            # clean ids
            ugly_ids = [corporation.data['corporation_id']]
            try:
                ugly_ids.append(corporation.data['alliance_id'])
            except:
                pass
            op = settings.ESI_APP.op['post_universe_names'](ids=ugly_ids)
            corporation = settings.ESI_CLIENT.request(op)


            self.character_corporation = corporation.data[0]['name']
            try:
                self.character_alliance = corporation.data[1]['name']
            except:
                pass
            self.save()
            return True
        except Exception as e:
            print(str(e))
            return False
