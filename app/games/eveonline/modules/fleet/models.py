from django.db import models
from django.conf import settings
from games.eveonline.models import EveCharacter
from games.eveonline.utils import generate_esi_session
import json, logging, datetime, time

logger = logging.getLogger(__name__)

# Create your models here.
class Fleet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fc = models.OneToOneField(EveCharacter, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now=True)
    # Additional information
    type = models.CharField(max_length=255, choices=settings.EVE_FLEET_TYPES, null=True, blank=True)
    value = models.DecimalField(max_digits=2, decimal_places=1)
    aar = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.fc.token.refresh()
        # Generate new ESI session
        esi_session = generate_esi_session()
        esi_session['security'].update_token(self.fc.token.populate())
        operation = esi_session['app'].op['get_characters_character_id_fleet'](character_id=self.fc.token.character_id)
        response = esi_session['client'].request(operation)
        if response.status == 200:
            self.id = response.data['fleet_id']
            new_settings = {"motd": "Krypted Fleet tracking has been enabled."}
            operation = esi_session['app'].op['put_fleets_fleet_id'](fleet_id=self.id, new_settings=new_settings)
            response = esi_session['client'].request(operation)
            super(Fleet, self).save(*args, **kwargs)
        else:
            logger.error("Error creating fleet. %s" % response.data)

    def track(self):
        self.fc.token.refresh()
        esi_session = generate_esi_session()
        esi_session['security'].update_token(eve_character.token.populate())
        operation = esi_session['app'].op['fleets_fleet_id_members'](fleet_id=self.id)
        response = esi_session['client'].request(operation)
        if response.status_code == 200:
            members = response.json()
            max_value = self.value * 0.5
            point_sheet = {}
            for member in members:
                eve_character = EveCharacter.objects.get(character_id=member['character_id']).get_absolute()
                if eve_character.character_id in point_sheet:
                    if point_sheet[eve_character.character_id] < max_value:
                        point_sheet[eve_character.character_id] += self.value * 0.5
                else:
                    point_sheet[eve_character.character_id] = self.value
            for member in point_sheet:
                FleetPont(character=EveCharacter.objects.get(character_id=member), value=point_sheet[member]).save()

    class Meta:
        permissions = (
                ('view_fleet', u'Can view a fleet.'),
                ('view_all_fleets', u'Can create a fleet.'),
        )

class FleetPoint(models.Model):
    value = models.DecimalField(max_digits=2, decimal_places=1)
    fleet = models.OneToOneField("Fleet", on_delete=models.CASCADE)
    character = models.OneToOneField(EveCharacter, null=True, on_delete=models.CASCADE)
