from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib import messages
from core.decorators import login_required, tutorial_complete, permission_required
from games.eveonline.models import Token, EveCharacter
# from games.eveonline.modules.fleet.models import Fleet, FleetPoint
from games.eveonline.utils import generate_esi_session
# from games.eveonline.modules.fleet.forms import FleetForm
import json, logging, datetime, time

logger = logging.getLogger(__name__)

@login_required
@permission_required('games.eveonline.modules.fleet.view_all_fleets')
def view_fleets(request):
    fleets = Fleet.objects.all()
    return render(
        request,
        'eveonline/modules/fleet/view_fleet.html',
        context={
            'fleets': fleets
        }
    )

@login_required
@permission_required('games.eveonline.modules.fleet.add_fleet')
def create_fleet(request):
    # Pull EVE Character & Update Token
    eve_character = EveCharacter.objects.get(request.user, main=None)
    Fleet(fc=eve_character).save()

@login_required
@permission_required('games.eveonline.modules.fleet.change_fleet')
def edit_fleet(request, fleet_id):
    fleet = Fleet.objects.get(id=fleet_id)
    eve_character = EveCharacter.objects.get(request.user, main=None)
    # Catch silly users
    if eve_character != fleet.fc:
        messages.add_message(request, messages.ERROR, 'You are not the owner of this fleet.')
        return redirect('view-fleets')
    # Edit fleet
    if request.method == 'POST':
        fleet.type = request.POST.get('type')
        fleet.aar = request.POST.get('aar')
        fleet.save()
        messages.add_message(request, messages.SUCCESS, 'Fleet updated.')
        return redirect('view-fleets')
    else:
        form = FleetForm()
    # Return webpage
    return render(
        request,
        'eveonline/modules/fleet/change_fleet.html',
        context = {
            'form': form,
            'fleet': fleet
        }
    )

@login_required
@permission_required('games.eveonline.modules.fleet.delete_fleet')
def delete_fleet(request, fleet_id):
    fleet = Fleet.objects.get(id=fleet_id)
    eve_character = EveCharacter.objects.get(request.user, main=None)
    if eve_character != fleet.fc:
        fleet.delete()
        messages.add_message(request, messages.SUCCESS, 'Fleet deleted.')
        return redirect('view-fleets')
    else:
        messages.add_message(request, messages.ERROR, 'You are not the owner of this fleet.')
        return redirect('view-fleets')

@login_required
@permission_required('games.eveonline.modules.fleet.view_fleet')
def view_fleet(request, fleet_id):
    fleet = Fleet.objects.get(id=fleet_id)
    eve_character = EveCharacter.objects.get(request.user, main=None)
    return render(
        request,
        'eveonline/modules/fleet/view_fleet.html',
        context={
            'fleet': fleet
        }
    )
