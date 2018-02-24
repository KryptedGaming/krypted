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
    tokens = Token.objects.all()
    for token in tokens:
        verify_sso_token(token)


@task()
def sync_users():
    logger.info("Bulk updating all users for EVE Online roles")
    verify_sso_tokens()         # make sure tokens are valid
    for user in User.objects.all():
        if Token.objects.filter(user=user).count() > 0:
            sync_user(user)


"""
MINOR TASKS
These tasks build the above tasks.
"""
@task()
def verify_sso_token(token):
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
        sync_user(token.user)

@task()
def sync_user(user):
    logger.info("Syncing user %s for EVE Online..." % user.username)
    # Get user information
    profile = Profile.objects.get(user=user)
    tokens = Token.objects.filter(user=user)
    characters = EveCharacter.objects.filter(user=user)
    group_clear = True
    eve_online_group = Group.objects.get(name=settings.EVE_ONLINE_GROUP)

    # Determine if member should have access
    for character in characters:
        character.update_corporation()
        if settings.EVE_ORGANIZATION_MODE == "CORPORATION":
            if character.character_corporation in settings.VERIFIED_CORPORATIONS:
                group_clear = False
        else:
            if character.character_alliance in settings.VERIFIED_CORPORATIONS:
                group_clear = False

    # Update user groups
    if group_clear:
        logger.info("Removing EVE Online role for %s" % user.username)
        user.groups.remove(Group.objects.get(name=eve_online_group.name))
        profile.guilds.remove(Guild.objects.get(group=eve_online_group))
    else:
        logger.info("Adding EVE Online role for %s" % user.username)
        user.groups.add(eve_online_group)
        profile.guilds.add(Guild.objects.get(group=eve_online_group))
    logger.info("")
