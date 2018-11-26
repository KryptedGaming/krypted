from django.shortcuts import render,redirect, get_object_or_404
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
from app.conf import eve as eve_settings
from games.eveonline.models import Token, EveCharacter
from core.models import User
from core.decorators import login_required
from games.eveonline.tasks import *

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def add_token(request):
    return redirect(eve_settings.ESI_URL_CACHE)

@login_required
def remove_token(request, character):
    eve_character = EveCharacter.objects.get(user=request.user, character_id=character)
    eve_character.token.delete()
    update_user_groups(eve_character.user.pk)
    return redirect('eve-dashboard')

@login_required
def refresh_token(request, character):
    eve_character = EveCharacter.objects.get(user=request.user, character_id=character)
    update_eve_token(eve_character.token.pk)
    update_eve_character(eve_character.pk)
    update_user_groups(eve_character.user.pk)
    return redirect('eve-dashboard')

def receive_token(request):
    if request.user.is_authenticated:
        ## SSO PROCESS
        code = request.GET.get('code', None)
        esi_token = eve_settings.ESI_SECURITY.auth(code)
        esi_verified = eve_settings.ESI_SECURITY.verify()

        ## CHECK IF TOKEN OF SAME CHARACTER EXISTS
        if EveCharacter.objects.filter(character_name=esi_verified['CharacterName']).count() > 0:
            eve_character = EveCharacter.objects.get(character_name=esi_verified['CharacterName'])
            eve_character.delete()

        ## CREATE TOKEN
        logger.info(
                "Creating token...\n" +
                "Lengths: " + "R: " + str(len(str(esi_token['refresh_token']))))
        token = Token(
                access_token=esi_token['access_token'],
                refresh_token=esi_token['refresh_token'],
                expires_in=esi_token['expires_in'],
                )
        token.save()

        ## CREATE CHARACTER
        op = eve_settings.ESI_APP.op['get_characters_character_id_portrait'](character_id=esi_verified['CharacterID'])
        portrait = eve_settings.ESI_CLIENT.request(op)

        try:
            eve_main_character = EveCharacter.objects.get(main=None, user=request.user)
        except:
            eve_main_character = None

        character = EveCharacter(
                character_id=esi_verified['CharacterID'],
                character_name=esi_verified['CharacterName'],
                character_portrait=portrait.data['px64x64'].replace("http", "https"),
                main=eve_main_character,
                token=token,
                user=request.user
        )

        character.save()
        character.update_corporation()
        update_user_groups(request.user.pk)
        return redirect('/eve')
    else:
        return redirect('login')
