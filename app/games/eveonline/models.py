from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, Group
import datetime

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

    def update_corporation(self, corporation_id):
        from django.core.exceptions import ObjectDoesNotExist
        op = settings.ESI_APP.op['get_corporations_corporation_id'](corporation_id=self.corporation_id)
        op = settings.ESI_CLIENT.request(op)
        corporation = settings.ESI_CLIENT.request(op)
        self.name = corporation.data['name']
        self.ticker = corporation.data['ticker']
        self.member_count = corporation.data['member_count']
        try:
            ceo = EveCharacter.objects.get(token__character_id = corporation.data['ceo'])
        except ObjectDoesNotExist:
            ceo = None
        self.ceo = ceo
        try:
            self.alliance_id = corporation.data['alliance_id']
        except:
            self.alliance_id = None
        self.tax_rate = corporation.data['tax_rate']
        self.save()

class EveCharacter(models.Model):
    character_name = models.CharField(max_length=255, primary_key=True)
    character_portrait = models.URLField(max_length=255, blank=True, null=True)
    character_alt_type = models.CharField(max_length=255, choices=settings.EVE_ALT_TYPES, null=True)
    corporation = models.ForeignKey("EveCorporation", null=True, on_delete=models.CASCADE)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.character_name

    def update_corporation(self):
        if not self.corporation:
            from django.core.exceptions import ObjectDoesNotExist
            # Pull the character information
            self.token.refresh()
            esi_app = settings.ESI_APP
            esi_security = settings.ESI_SECURITY
            esi_security.update_token(self.token.populate())
            op = esi_app.op['get_characters_character_id'](character_id=self.token.character_id)
            character = settings.ESI_CLIENT.request(op)
            # Build the corporation if needed
            if EveCorporation.objects.filter(corporation_id=character.data['corporation_id']).exists():
                self.corporation = EveCorporation.objects.get(corporation_id=character.data['corporation_id'])
                self.save()
            else:
                op = esi_app.op['get_corporations_corporation_id'](corporation_id=character.data['corporation_id'])
                corporation = settings.ESI_CLIENT.request(op)
                eve_corporation = EveCorporation(
                    corporation_id = character.data['corporation_id'],
                    name = corporation.data['name'],
                    ticker = corporation.data['ticker'],
                    member_count = corporation.data['member_count'],
                    tax_rate = corporation.data['tax_rate']
                )
                try:
                 eve_corporation.ceo = EveCharacter.objects.get(token__character_id = corporation.data['ceo_id'])
                except ObjectDoesNotExist:
                 eve_corporation.ceo = None
                try:
                    eve_corporation.alliance_id = corporation.data['alliance_id'],
                except:
                    eve_corporation.alliance_id = None
                eve_corporation.save()
                self.corporation = eve_corporation
                self.save()
        else:
            self.token.refresh()
            op = settings.ESI_APP.op['get_characters_character_id'](character_id=self.token.character_id)
            character = settings.ESI_CLIENT.request(op)
            if self.corporation.corporation_id != character.data['corporation_id']:
                self.corporation.corporation_id = None
                self.save()
                self.update_corporation()

    def get_absolute(self):
        """
        Ensures that we return the main character
        """
        if self.main:
            return self.main
        else:
            return self
