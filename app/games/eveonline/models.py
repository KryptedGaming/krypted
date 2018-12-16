
from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import User, Group
from app.conf import eve as eve_settings
import datetime
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class Token(models.Model):
    ## SSO
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    expires_in = models.IntegerField(default=0)
    expiry = models.DateTimeField(blank=True, null=False, auto_now_add=True)
    scopes = models.TextField(blank=True, null=True)

    @staticmethod
    def format_scopes(scopes):
        if type(scopes) is str:
            return scopes.split(",")
        else:
            return ",".join(scopes)

    def populate(self):
        data = {}
        data['access_token'] = self.access_token
        data['refresh_token'] = self.refresh_token
        data['expires_in'] = self.expires_in

        return data

    def refresh(self):
        if timezone.now() > self.expiry:
            try:
                eve_settings.ESI_SECURITY.update_token(self.populate())
                new_token = eve_settings.ESI_SECURITY.refresh()
                self.access_token = new_token['access_token']
                self.refresh_token = new_token['refresh_token']
                self.expiry = timezone.now() + datetime.timedelta(0, new_token['expires_in'])
                self.save()
            except Exception as e:
                print(e.response)
                if e.response['error'] == 'invalid_token':
                    self.delete()
        else:
            logger.info("Token refresh not needed")

    def force_refresh(self):
        try:
            eve_settings.ESI_SECURITY.update_token(self.populate())
            new_token = eve_settings.ESI_SECURITY.refresh()
            self.access_token = new_token['access_token']
            self.refresh_token = new_token['refresh_token']
            self.expiry = timezone.now() + datetime.timedelta(0, new_token['expires_in'])
            self.save()
            return True
        except:
            self.delete()
            return False

class EveCorporation(models.Model):
    corporation_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512)
    ticker = models.CharField(max_length=5)
    member_count = models.IntegerField()
    ceo = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.SET_NULL) # optional if we dont have them yet
    alliance_id = models.IntegerField(null=True)
    tax_rate = models.FloatField()

    def __str__(self):
        return self.name

class EveCharacter(models.Model):
    character_id = models.IntegerField()
    character_name = models.CharField(max_length=255)
    character_portrait = models.URLField(max_length=255, blank=True, null=True)
    character_alt_type = models.CharField(max_length=255, choices=eve_settings.EVE_ALT_TYPES, null=True, blank=True)
    corporation = models.ForeignKey("EveCorporation", null=True, on_delete=models.SET_NULL)

    ## SSO Token
    token = models.OneToOneField("Token", null=True, on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.character_name

    def is_member(self):
        if self.corporation and (self.corporation.corporation_id == eve_settings.MAIN_ENTITY_ID or self.corporation.corporation_id in eve_settings.SECONDARY_ENTITY_IDS):
            return True
        else:
            return False

    def get_absolute(self):
        """
        Ensures that we return the main character
        """
        if self.main:
            return self.main
        else:
            return self

    class Meta:
        permissions = (
            ('audit_eve_character', u'Can audit an EVE character.'),
        )
