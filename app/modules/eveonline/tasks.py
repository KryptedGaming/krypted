from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.apps import apps
# INTERNAL IMPORTS
from modules.eveonline.models import EveToken, EveCharacter, EveCorporation
from modules.eveonline.client import EveClient
# MISC
from esipy import App
import logging, time, datetime, pytz

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def update_sso_tokens():
    tokens = EveToken.objects.all()
    for token in tokens:
        update_eve_token.apply_async(args=[token.pk])

@task()
def update_eve_characters():
    for character in EveCharacter.objects.filter(~Q(token=None)):
        update_character.apply_async(args=[character.character_id])

@task()
def update_eve_character_corporations():
    for character in EveCharacter.objects.filter(~Q(token=None)):
        update_character_corporation.apply_async(args=[character.character_id])
        
"""
MINOR TASKS
Small tasks
"""
@task()
def update_character(character_id):
    # query ESI
    response = EveClient().get_character(character_id)
    if response.status != 200:
        logger.warning("ESI Error: %s" % response.data)
        return
    # update existing character or create new one
    if EveCharacter.objects.filter(character_id=character_id).exists():
        character = EveCharacter.objects.get(character_id=character_id)
        character.character_portrait = response.data['portrait']
    else:
        character = EveCharacter(
            character_id=character_id,
            character_name=response.data['name'],
            character_portrait=response.data['portrait'],
        )
    character.save()

@task()
def update_character_corporation(character_id):
    # query ESI
    response = EveClient().get_character(character_id)
    if response.status != 200:
        logger.warning("ESI Error: %s" % response.data)
        return
    # update corporation
    if EveCorporation.objects.filter(corporation_id=response.data['corporation_id']).exists():
        character = EveCharacter.objects.get(character_id=character_id)
        character.corporation = EveCorporation.objects.get(corporation_id=response.data['corporation_id'])
    else:
        character = EveCharacter.objects.get(character_id=character_id)
        update_corporation(response.data['corporation_id'])
        character.corporation = EveCorporation.objects.get(corporation_id=response.data['corporation_id'])
    character.save()


@task()
def update_corporation(corporation_id):
    # query ESI
    response = EveClient().get_corporation(corporation_id)
    if response.status != 200:
        logger.warning("ESI Error: %s" % response.data)
        return
    # update existing corporation or create new one
    if EveCorporation.objects.filter(corporation_id=corporation_id).exists():
        corporation = EveCorporation.objects.get(corporation_id=corporation_id)
        corporation.member_count=response.data['member_count']
        # add alliance id
        if 'alliance_id' in response.data:
            corporation.alliance_id=response.data['alliance_id']
        else:
            corporation.alliance_id=None
        corporation.tax_rate=response.data['tax_rate']
        # update CEO
        if EveCharacter.objects.filter(character_id=response.data['ceo_id']).exists():
            corporation.ceo = EveCharacter.objects.get(character_id=response.data['ceo_id'])
        else:
            update_character(response.data['ceo_id'])
            corporation.ceo = EveCharacter.objects.get(character_id=response.data['ceo_id'])
    else:
        corporation = EveCorporation(
            name=response.data['name'],
            corporation_id=corporation_id,
            ticker=response.data['ticker'],
            member_count=response.data['member_count'],
            tax_rate=response.data['tax_rate']
        )
        # add alliance id
        if 'alliance_id' in response.data:
            corporation.alliance_id=response.data['alliance_id']
        else:
            corporation.alliance_id=None
        # update CEO
        if EveCharacter.objects.filter(character_id=response.data['ceo_id']).exists():
            corporation.ceo = EveCharacter.objects.get(character_id=response.data['ceo_id'])
        else:
            update_character(response.data['ceo_id'])
            corporation.ceo = EveCharacter.objects.get(character_id=response.data['ceo_id'])
    corporation.save()

@task()
def update_eve_token(pk):
    eve_token = EveToken.objects.get(pk=pk)
    eve_token.refresh()

def audit_corporation_members():
    response = []
    missing = []
    characters = EveClient().get_corporation_characters(eve_settings.MAIN_ENTITY_ID)
    secondary_characters = EveClient().get_corporation_characters(eve_settings.SECONDARY_ENTITY_IDS[0])
    for character in characters:
        if not EveCharacter.objects.filter(character_id=character).exists():
            missing.append(character)
    for character in secondary_characters:
        if not EveCharacter.objects.filter(character_id=character).exists():
            missing.append(character)
    ESI_APP = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')
    op = ESI_APP.op['post_universe_names'](ids=missing)
    character_names = eve_settings.ESI_CLIENT.request(op).data
    for character_name in character_names:
        response.append(character_name['name'])
    return response