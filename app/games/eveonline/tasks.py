from __future__ import absolute_import, unicode_literals
from celery import task
from games.eveonline.models import Token, EveCharacter, EveCorporation
from games.eveonline.client import EveClient
from core.models import User, Group
from core.models import Guild
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
from app.conf import eve as eve_settings
from django.db.models import Q
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def update_sso_tokens():
    tokens = Token.objects.all()
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
def update_users_groups():
    guild = Guild.objects.get(slug='eve')
    call_count = 0
    for user in User.objects.filter(guilds__name='EVE Online'):
        update_user_groups.apply_async(args=[user.pk], coundown=call_count*2)
        call_count += 1

"""
MINOR TASKS
Small tasks
"""
@task()
def update_character(character_id):
    # query ESI
    response = EveClient.get_character(character_id)
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
    response = EveClient.get_character(character_id)
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
    response = EveClient.get_corporation(corporation_id)
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
    eve_token = Token.objects.get(pk=pk)
    eve_token.refresh()

@task()
def update_user_groups(pk):
    user = User.objects.get(pk=pk)
    guild = Guild.objects.get(slug='eve')
    if EveCharacter.objects.filter(user=user).count() < 1:
        remove_eve_groups(user)
    else:
        eve_character = EveCharacter.objects.get(user=user, main=None)
        if eve_character.is_member():
            user.groups.add(guild.group)
            user.guilds.add(guild)
        else:
            remove_eve_groups(user)

# HELPERS
def remove_eve_groups(user):
    guild = Guild.objects.get(slug="eve")
    guild_groups = Group.objects.filter(guild=guild)
    if guild.group in user.groups.all():
        user.groups.remove(guild.group)
    for group in guild_groups:
        if group in user.groups.all():
            user.groups.remove(group)
        time.sleep(1)
    user.guilds.remove(guild)

def audit_corporation_members():
    response = []
    missing = []
    characters = EveClient.get_corporation_characters(eve_settings.MAIN_ENTITY_ID)
    secondary_characters = EveClient.get_corporation_characters(eve_settings.SECONDARY_ENTITY_IDS[0])
    for character in characters:
        if not EveCharacter.objects.filter(character_id=character).exists():
            missing.append(character)
    for character in secondary_characters:
        if not EveCharacter.objects.filter(character_id=character).exists():
            missing.append(character)
    op = eve_settings.ESI_APP.op['post_universe_names'](ids=missing)
    character_names = eve_settings.ESI_CLIENT.request(op).data
    for character_name in character_names:
        response.append(character_name['name'])
    return response
