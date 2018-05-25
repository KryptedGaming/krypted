from django.db import models
from django.conf import settings

# Create your models here.
class Fleet(models.Models):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255, choices=settings.EVE_FLEET_TYPES, null=True, blank=True)
    fc = models.OneToOneField(EveCharacter, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now=True)

class FleetPoint(models.Model):
    fleet = models.OneToOneField("Fleet")
    character_id = models.IntegerField()
