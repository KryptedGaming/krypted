from __future__ import absolute_import, unicode_literals
from celery import task
from games.eveonline.models import Token, EveCharacter
from core.models import User, Group
from core.models import Guild
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
from app.conf import eve as eve_settings
import logging, time

logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def verify_sso_tokens():
    logger.info("Verifying all SSO tokens")
    tokens = Token.objects.all()
    for token in tokens:
        verify_sso_token.apply_async(args=[token.character_id])


@task()
def sync_users():
    logger.info("Bulk updating all users for EVE Online roles")
    call_count = 0
    for user in User.objects.filter(groups__name=eve_settings.EVE_ONLINE_GROUP):
        logger.info("Syncing EVE Online permissions for %s" % user.username)
        if Token.objects.filter(user=user).count() > 0:
            sync_user.apply_async(args=[user.pk], countdown=call_count*10)
            call_count += 1
        else:
            eve_guild = Guild.objects.get(slug="eve")
            try:
                if eve_guild.group in user.groups.all():
                    sync_user.apply_async(args=[user.pk], countdown=call_count*10)
            except Exception as e:
                logger.error("Error when syncing EVE user. %s" % e)

"""
MINOR TASKS
These tasks build the above tasks.
"""
@task()
def verify_sso_token(character_id):
    token = Token.objects.get(character_id=character_id)
    character = EveCharacter.objects.get(token=token)
    eve_settings.ESI_SECURITY.update_token(token.populate())
    logger.info("Syncing token for %s" % character.character_name)
    try:
        eve_settings.ESI_SECURITY.refresh()
        character.update_corporation()
        sync_user.apply_async(args=[token.user.pk], countdown=10)
    except Exception as e:
        logger.info("Token of %s expired for %s. %s" % (character, token.user, e))
        character.character_corporation = "ERROR"
        character.character_alliance = "ERROR"
        character.save()
        sync_user.apply_async(args=[token.user.pk])

@task()
def sync_user(user):
    # Get user information
    user = User.objects.get(pk=user)
    guild = Guild.objects.get(slug="eve")
    logger.info("Syncing user %s for EVE Online..." % user.username)
    if not EveCharacter.objects.filter(main=None, user=user):
        clear_eve_groups(user)
    else:
        main_character = EveCharacter.objects.get(main=None, user=user)
        in_main_corporation = str(main_character.corporation.corporation_id) in eve_settings.MAIN_ENTITY_ID
        in_secondary_corporation = str(main_character.corporation.corporation_id) in eve_settings.SECONDARY_ENTITY_IDS

        if in_main_corporation or in_secondary_corporation:
            user.groups.add(guild.group)

        if not in_main_corporation and not in_secondary_corporation:
            clear_eve_groups(user)

def clear_eve_groups(user):
    guild = Guild.objects.get(slug="eve")
    guild_groups = Group.objects.filter(guild=guild)
    for group in guild_groups:
        if group in user.groups.all():
            user.groups.remove(group)
        time.sleep(1)
    user.groups.remove(guild.group)
