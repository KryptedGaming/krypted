from django.shortcuts import redirect
from django.apps import apps
from django.contrib.auth.decorators import login_required
# INTERNAL IMPORTS
from modules.eveonline.models import EveToken, EveCharacter
from modules.eveonline.tasks import *

import logging
eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

# Create your views here.
def add_token(request):
    return redirect(eve_settings.ESI_URL_CACHE)

@login_required
def remove_token(request, character):
    eve_character = EveCharacter.objects.get(user=request.user, character_id=character)
    eve_character.token.delete()
    return redirect('eve-dashboard')

@login_required
def refresh_token(request, character):
    eve_character = EveCharacter.objects.get(user=request.user, character_id=character)
    update_eve_token.apply_async(args=[eve_character.token.pk])
    update_character.apply_async(args=[eve_character.character_id])
    update_character_corporation.apply(args=[eve_character.character_id])
    return redirect('eve-dashboard')

@login_required
def receive_token(request):
    ## SSO PROCESS
    code = request.GET.get('code', None)
    esi_token = eve_settings.ESI_SECURITY.auth(code)
    esi_verified = eve_settings.ESI_SECURITY.verify()

    ## CREATE TOKEN
    logger.info(
            "Creating token...\n" +
            "Lengths: " + "R: " + str(len(str(esi_token['refresh_token']))))
    token = EveToken(
            access_token=esi_token['access_token'],
            refresh_token=esi_token['refresh_token'],
            expires_in=esi_token['expires_in'],
            scopes=EveToken.format_scopes(eve_settings.ESI_SCOPES)
            )
    token.save()

    # PULL MAIN CHARACTER
    if EveCharacter.objects.filter(user=request.user, main=None).count() > 0:
        eve_main_character = EveCharacter.objects.get(user=request.user, main=None)
    else:
        eve_main_character = None
    ## CHECK IF TOKEN OF SAME CHARACTER EXISTS
    if EveCharacter.objects.filter(character_name=esi_verified['name']).count() > 0:
        character = EveCharacter.objects.get(character_name=esi_verified['name'])
        character.token = token
    else:
        character = EveCharacter(
                character_id=esi_verified['sub'].split(":")[-1],
                character_name=esi_verified['name'],
                main=eve_main_character,
                token=token,
                user=request.user
        )

    character.save()
    update_character.apply_async(args=[character.character_id])
    update_character_corporation.apply_async(args=[character.character_id])
    if apps.is_installed('modules.eveonline.extensions.eveaudit'):
        from modules.eveonline.extensions.eveaudit.tasks import update_character_data
        update_character_data.apply_async(args=[character.character_id])
    if 'eve_sso_redirect_override' in request.session:
        override = request.session['eve_sso_redirect_override']
        request.session.pop('eve_sso_redirect_override')
        return redirect(override)
    return redirect('/eve')
