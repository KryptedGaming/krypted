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
def update_sso_tokens():
    logger.info("Verifying all SSO tokens")
    tokens = Token.objects.all()
    for token in tokens:
        update_eve_token.apply_async(args=[token.pk])

@task()
def update_eve_characters():
    for character in EveCharacter.objects.all():
        update_eve_character.apply_async(args=[character.pk])

@task()
def update_users_groups():
    guild = Guild.objects.get(slug='eve')
    call_count = 0
    for user in User.objects.all():
        if guild in user.guilds.all():
            if Token.objects.filter(user=user).count() > 0:
                update_user_groups.apply_async(args=[user.pk], coundown=call_count*5)
                call_count += 1
            else:
                remove_eve_groups(user)
        else:
            remove_eve_groups(user)

@task()
def update_eve_token(pk):
    eve_token = Token.objects.get(pk=pk)
    eve_token.refresh()

@task()
def update_eve_character(pk):
    eve_character=EveCharacter.objects.get(pk=pk)
    eve_character.update_corporation()

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
