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

    def refresh(self):

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

class EveCharacter(models.Model):
    character_name = models.CharField(max_length=256, primary_key=True)
    character_portrait = models.URLField(max_length=256, blank=True, null=True)

    ## SSO Token
    token = models.OneToOneField("Token", on_delete=models.CASCADE)

    ## CORE
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ## ALTERNATE CHARACTER
    main = models.ForeignKey("EveCharacter", blank=True, null=True)

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
