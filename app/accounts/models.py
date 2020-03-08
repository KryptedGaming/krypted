import uuid
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.conf import settings

class UserInfo(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="info")
    country = CountryField(default="US")
    age = models.IntegerField(default=18)
    secret = models.UUIDField(default=uuid.uuid4)

    def display_name(self):
        try:
            settings.DISPLAY_NAME
        except Exception as e:
            return self.user.username 
        if settings.DISPLAY_NAME and settings.DISPLAY_NAME == "DISCORD" and "django_discord_connector" in settings.INSTALLED_APPS and self.user.discord_token:
            return self.user.discord_token.discord_user.nickname
        elif settings.DISPLAY_NAME and settings.DISPLAY_NAME == "EVEONLINE" and "django_eveonline_connector" in settings.INSTALLED_APPS and self.get_eveonline_character():
            self.user.primary_evecharacter.character
        return self.user.username 
    
    def display_avatar(self):
        if "django_eveonline_connector" in settings.INSTALLED_APPS:
            if self.user.primary_evecharacter:
                return self.user.primary_evecharacter.character.avatar
        return "https://api.adorable.io/avatars/160/%s.png" % self.user.username 
