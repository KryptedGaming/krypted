from django.db import models
from django.conf import settings
from core.models import Event
from games.eveonline.models import EveCharacter
from games.eveonline.utils import generate_esi_session

import json, logging, datetime, time
logger = logging.getLogger(__name__)

# Create your models here.
class Fleet(Event):
    eve_id = models.BigIntegerField()
    fc = models.OneToOneField(EveCharacter, null=True, on_delete=models.SET_NULL)

    # Additional information
    type = models.CharField(max_length=255, choices=settings.EVE_FLEET_TYPES, null=True, blank=True)
    aar = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # set the FC
        try:
            self.fc = EveCharacter.objects.get(user=self.creator, main=None)
        except Exception as e:
            logger.error("Exception when setting FC of fleet. %s" % e)

        # assign the point values
        print(self.type)
        self.value = settings.EVE_FLEET_VALUES[self.type]

        # set the EVE_ID
        self.fc.token.refresh()
        # Generate new ESI session
        esi_session = generate_esi_session()
        esi_session['security'].update_token(self.fc.token.populate())
        operation = esi_session['app'].op['get_characters_character_id_fleet'](character_id=self.fc.token.character_id)
        response = esi_session['client'].request(operation)
        if response.status == 200:
            self.eve_id = response.data['fleet_id']
            new_settings = {"motd": "Fleet tracking has been enabled."}
            print("setting motd")
            operation = esi_session['app'].op['put_fleets_fleet_id'](fleet_id=self.id, new_settings=new_settings)
            response = esi_session['client'].request(operation)
            super(Fleet, self).save(*args, **kwargs)
        else:
            logger.error("Error creating fleet. %s" % response.data)

    def track(self):
        self.fc.token.refresh()
        esi_session = generate_esi_session()
        esi_session['security'].update_token(self.fc.token.populate())
        operation = esi_session['app'].op['get_fleets_fleet_id_members'](fleet_id=self.id)
        response = esi_session['client'].request(operation)
        print(response.status)
        print(response.data)
        print(response.raw)
        if response.status == 200:
            members = response.data
            for member in members:
                member = EveCharacter.objects.get(character_id=member['character_id']).get_absolute()
                print("creating fleetpoint for %s" % member)
                FleetPont(character=member, value=self.value).save()

    class Meta:
        permissions = (
                ('view_fleet', u'Can view a fleet.'),
                ('view_all_fleets', u'Can create a fleet.'),
        )

class FleetPoint(models.Model):
    value = models.DecimalField(max_digits=2, decimal_places=1)
    fleet = models.OneToOneField("Fleet", on_delete=models.CASCADE)
    character = models.OneToOneField(EveCharacter, null=True, on_delete=models.CASCADE)
