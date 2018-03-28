from __future__ import absolute_import, unicode_literals
from celery import task
from games.eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Profile, Guild
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
import logging

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
    for user in User.objects.all():
        logger.info("Syncing EVE Online permissions for %s" % user.username)
        if Token.objects.filter(user=user).count() > 0:
            sync_user.apply_async(args=[user.pk])
        else:
            try:
                profile = Profile.objects.get(user=user)
                profile.guilds.remove(Guild.objects.get(group__name=settings.EVE_ONLINE_GROUP))
            except:
                pass
            user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
            user.groups.remove(Group.objects.get(name=settings.MAIN_GROUP))
            user.groups.remove(Group.objects.get(name=settings.MINOR_GROUP))
            user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))



"""
MINOR TASKS
These tasks build the above tasks.
"""
@task()
def verify_sso_token(character_id):
    token = Token.objects.get(character_id=character_id)
    character = EveCharacter.objects.get(token=token)
    settings.ESI_SECURITY.update_token(token.populate())
    logger.info("Syncing token for %s" % character.character_name)
    try:
        settings.ESI_SECURITY.refresh()
    except Exception as e:
        logger.info("Token of %s expired for %s" % (character, token.user))
        character.character_corporation = "ERROR"
        character.character_alliance = "ERROR"
        character.save()
        sync_user.apply_sync(args=[token.user.pk])

@task()
def sync_user(user):
    # Get user information
    user = User.objects.get(pk=user)
    logger.info("Syncing user %s for EVE Online..." % user.username)
    profile = Profile.objects.get(user=user)
    tokens = Token.objects.filter(user=user)
    characters = EveCharacter.objects.filter(user=user)
    group_clear = True
    eve_online_group = Group.objects.get(name=settings.EVE_ONLINE_GROUP)

    # Determine if member should have access
    groups = []

    for character in characters:
        character.update_corporation()
        logger.info("ALLIANCE MODE: %s" % settings.ALLIANCE_MODE)
        if settings.ALLIANCE_MODE:
            logger.info("ALLIANCE MODE ENABLED... Checking Alliance IDs.")
            if str(character.corporation.alliance_id) in settings.MAIN_ENTITY_ID:
                logger.info("Alliance mode, case 1.")
                groups.append(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                groups.append(Group.objects.get(name=settings.MAIN_GROUP))
                group_clear = False
            elif str(character.corporation.alliance_id) in settings.SECONDARY_ENTITY_IDS:
                logger.info("Alliance mode, case 2.")
                groups.append(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                groups.append(Group.objects.get(name=settings.MINOR_GROUP))
                group_clear = False
            else:
                logger.info("Alliance mode, case 3.")
        else:
            logger.info("CORPORATION MODE ENABLED... Checking Coporation IDs.")
            if str(character.corporation.corporation_id) in settings.MAIN_ENTITY_ID:
                logger.info("Corporation mode, case 1.")
                groups.append(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                groups.append(Group.objects.get(name=settings.MAIN_GROUP))
                group_clear = False
            elif str(character.corporation.corporation_id) in settings.SECONDARY_ENTITY_IDS:
                logger.info("Corporation mode, case 2.")
                groups.append(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
                groups.append(Group.objects.get(name=settings.MINOR_GROUP))
                group_clear = False
            else:
                logger.info("Corporation mode, case 3.")


    # Update user groups
    if group_clear:
        logger.info("Removing EVE Online role for %s" % user.username)
        user.groups.remove(Group.objects.get(name=settings.EVE_ONLINE_GROUP))
        user.groups.remove(Group.objects.get(name=settings.MAIN_GROUP))
        user.groups.remove(Group.objects.get(name=settings.MINOR_GROUP))
        user.groups.add(Group.objects.get(name=settings.GUEST_GROUP))
        profile.guilds.remove(Guild.objects.get(group=eve_online_group))
    else:
        logger.info("Adding EVE Online role for %s" % user.username)
        for group in groups:
            user.groups.add(group)
        user.groups.remove(Group.objects.get(name=settings.GUEST_GROUP))
        profile.guilds.add(Guild.objects.get(group=eve_online_group))
