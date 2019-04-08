# DJANGO IMPORTS
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.apps import apps
# MISC
import datetime, logging, json


eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

# Create your models here.
class EveToken(models.Model):
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
                response = json.loads(e.response.decode("utf-8"))
                if response["error"] == 'invalid_token' or response["error"] == 'invalid_grant: Token is expired or invalid.':
                    logger.warning("EVE token expired, deleting.")
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

    # INFORMATION
    name = models.CharField(max_length=512)
    ticker = models.CharField(max_length=5)
    member_count = models.IntegerField()
    alliance_id = models.IntegerField(blank=True, null=True)
    tax_rate = models.FloatField()

    # REFERENCES
    ceo = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.SET_NULL) # optional if we dont have them yet

    # INTEGRATIONS
    primary_entity = models.BooleanField(default=False)
    blue_entity = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_main_characters(self):
        return EveCharacter.objects.filter(corporation=self, main=None)

class EveCharacter(models.Model):
    character_id = models.IntegerField()
    character_name = models.CharField(max_length=255)
    character_portrait = models.URLField(max_length=255, blank=True, null=True)
    character_alt_type = models.CharField(max_length=255, choices=eve_settings.EVE_ALT_TYPES, null=True, blank=True)
    corporation = models.ForeignKey("EveCorporation", null=True, on_delete=models.SET_NULL)

    ## SSO Token
    token = models.OneToOneField("EveToken", null=True, on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.CASCADE, related_name="alts")

    def __str__(self):
        return self.character_name

    def is_member(self):
        character = self.get_absolute()
        if character.corporation.primary_entity:
            return True
        elif self.corporation.primary_entity:
            return True 
        else:
            return False

    def is_blue(self):
        character = self.get_absolute()
        if character.corporation.blue_entity:
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

    @staticmethod
    def get_eve_character(user):
        return EveCharacter.objects.filter(user=user, main=None).first()

class EveGroupIntegration(models.Model):
    character_status_choices = (
        ("PRIMARY", "PRIMARY"),
        ("BLUE", "BLUE"),
    )
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=character_status_choices, null=True, blank=True)
    corporations = models.ManyToManyField("EveCorporation", blank=True)
    character_alt_type = models.CharField(max_length=255, choices=eve_settings.EVE_ALT_TYPES, null=True, blank=True)
    
    def __str__(self):
        return self.group.name

    def audit_user(self, user):
        logger.debug("Auditing Group Integration %s for user %s" % (self, user))
        if user.evecharacter_set.all().count() < 1:
            logger.debug("Failed EVE group integration: NO_EVE_CHARACTERS")
            return False 
        if self.status:
            if self.status == "PRIMARY":
                primary_check = False 
                for eve_character in user.evecharacter_set.all():
                    if eve_character.is_member():
                        logger.debug("Failed EVE group integration: NOT_MEMBER")
                        primary_check=True 
                if not primary_check:
                    return False 
            if self.status == "BLUE":
                blue_check = False
                for eve_character in user.evecharacter_set.all():
                    if eve_character.is_blue():
                        logger.debug("Failed EVE group integration: NOT_BLUE")
                        blue_check = True 
                if not blue_check:
                    return False 
        if self.corporations.all():
            corporation_check = False 
            for eve_character in user.evecharacter_set.all():
                if eve_character.corporation in self.corporations.all():
                    logger.debug("Failed EVE group integration: NOT_IN_CORPORATION")
                    corporation_check = True 
            if not corporation_check:
                return False 
        if self.character_alt_type:
            if not EveCharacter.objects.filter(user=user, character_alt_type=self.character_alt_type).first():
                logger.debug("Failed EVE group integration: NOT_ALT_TYPE")
                return False 
        return True 
        


