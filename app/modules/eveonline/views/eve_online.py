# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.apps import apps
# INTERNAL IMPORTS
from modules.eveonline.models import EveToken, EveCharacter
# EXTERNAL IMPORTS
from operator import itemgetter
from esipy import EsiApp, App
import logging, time

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def dashboard(request):
    context = {}
    context['alt_types'] = eve_settings.EVE_ALT_TYPES
    logger.info("User connected to the EVE dashboard.")
    return render(request, 'eveonline/dashboard.html', context)

@login_required
@permission_required('audit_eve_character')
def view_characters(request):
    context = {}
    active_eve_users = User.objects.filter(guilds__slug="eve")
    context['mains'] = EveCharacter.objects.filter(main=None, user__in=active_eve_users)
    context['dreads'] = EveCharacter.objects.filter(character_alt_type="dread_alt", user__in=active_eve_users)
    context['carriers'] = EveCharacter.objects.filter(character_alt_type="carrier_alt", user__in=active_eve_users)
    context['supers'] = EveCharacter.objects.filter(character_alt_type="super_alt", user__in=active_eve_users)
    context['faxes'] = EveCharacter.objects.filter(character_alt_type="fax_alt", user__in=active_eve_users)
    return render(request, 'eveonline/view_characters.html', context)


@login_required
@permission_required('audit_eve_character')
def view_character(request, character):
    context = {}
    context['character'] = eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
    return render(request, 'eveonline/view_character.html', context)

@login_required
def set_main_character(request, character):
    eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
    eve_alts = EveCharacter.objects.filter(~Q(character_id=character), user=request.user)
    eve_character.main = None
    eve_character.character_alt_type = None
    eve_character.save()
    for alt in eve_alts:
        alt.main = eve_character
        alt.character_alt_type = None
        alt.save()
    return redirect('eve-dashboard')

@login_required
def set_alt_character(request, character, alt_type):
    eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
    eve_character_main = EveCharacter.objects.get(user=request.user, main=None)
    eve_character.main = eve_character_main
    eve_character.character_alt_type = alt_type
    eve_character.save()
    return redirect('eve-dashboard')