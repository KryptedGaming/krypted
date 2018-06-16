from django import forms
from django.conf import settings
from games.eveonline.modules.fleet.models import Fleet

class FleetForm(forms.Form):
    type = forms.CharField(max_length=16, widget=forms.Select(choices=settings.EVE_FLEET_TYPES))
    aar = forms.URLField()
