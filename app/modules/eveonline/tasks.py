from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.apps import apps
# INTERNAL IMPORTS
from modules.eveonline.models import EveToken, EveCharacter, EveCorporation, EveCharacterData
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

@task()
def update_eve_characters_data():
    for character in EveCharacter.objects.filter(~Q(token=None)):
        if character.is_member() or character.is_blue():
            update_character_data.apply_async(args=[character.character_id])
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

@task()
def update_character_data(character_id):
    eve_client = EveClient()
    eve_character = EveCharacter.objects.get(character_id=character_id)
    logger.info("Updating Character Data for %s")
    eve_character_data = EveCharacterData.objects.get_or_create(character=eve_character)[0]
    # update skillpoints
    skillpoints = EveClient().get_character_skill_points(character_id)
    if skillpoints:
        eve_character_data.total_skillpoints = skillpoints
    # update wallet balance
    balance = EveClient().get_character_wallet_balance(character_id)
    if balance:
        eve_character_data.total_isk = balance
    # update contracts
    contracts = EveClient().get_character_contracts(character_id)
    if contracts:
        eve_character_data.contracts = contracts
    # update skill tree 
    skill_tree = EveClient().get_character_skill_tree(character_id)
    if skill_tree:
        eve_character_data.skill_tree = skill_tree
    # update journal 
    journal = EveClient().get_character_journal(character_id)
    if journal:
        eve_character_data.journal = journal
    # update contacts
    contacts = EveClient().get_character_contacts(character_id)
    if contacts:
        eve_character_data.contacts = contacts
    # update mails 
    mails = EveClient().get_character_mails(character_id)
    if mails:
        eve_character_data.mails = mails
    # update hangar assets
    hangar_assets = EveClient().get_character_hangar_assets(character_id)
    if hangar_assets:
        eve_character_data.assets = hangar_assets

    eve_character_data.save()
    
