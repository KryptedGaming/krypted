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
                return True
            except:
                self.delete()
                return False
        else:
            print("Token refresh not needed.")
            return True

class EveCharacter(models.Model):
    character_name = models.CharField(max_length=255, primary_key=True)
    character_portrait = models.URLField(max_length=255, blank=True, null=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.character_name

    def update_portrait(self):
        try:
            esi_app = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

            esi_security = EsiSecurity(
                app=esi_app,
                redirect_uri=settings.ESI_CALLBACK_URL,
                client_id=settings.ESI_CLIENT_ID,
                secret_key=settings.ESI_SECRET_KEY,
            )

            esi_client = EsiClient(esi_security)

            esi_security.update_token(self.populate())

            new_token = esi_security.refresh()
            self.access_token = new_token['access_token']
            self.refresh_token = new_token['refresh_token']
            return True

        except:
            self.delete()
            return False
