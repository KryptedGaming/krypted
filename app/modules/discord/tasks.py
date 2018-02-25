from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discord.models import *
from modules.discord.models import DiscordToken
from django.contrib.auth.models import User, Group
from modules.discord.utils import *
import logging

logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

OK_STATUS_CODES = [200, 201, 204]

@task(bind=True)
def add_discord_group(self, group):
    logger.info("Group received... %s" % group)
    group = Group.objects.get(pk=group)
    try:
        api_add_discord_group(group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)
@task(bind=True)
def remove_discord_group(self, group):
    group = Group.objects.get(pk=group)
    group = DiscordRole.objects.get(group=group)
    try:
        api_remove_discord_group(group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)
@task(bind=True)
def add_user_to_discord_group(self, user, group):
    logger.info("Adding %s to %s" % (user, group))
    user = User.objects.get(pk=user)
    group = DiscordRole.objects.get(role_id=group)
    try:
        api_add_user_to_discord_group(user, group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)
@task(bind=True)
def remove_user_from_discord_group(self, user, group):
    logger.info("Removing %s from %s" % (user, group))
    user = User.objects.get(pk=user)
    group = DiscordRole.objects.get(role_id=group)
    try:
        api_remove_user_from_discord_group(user, group)
    except RateLimitException as e:
        self.retry(exc=e, countdown=60)

# Helpers
def api_add_discord_group(group):
    """
    Expects a string role_name and a Group object.
    Creates a Discord Group in the auth database, as well as the Discord server.
    """
    logger.info("passed in %s" % group)
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
    # Set channel name
    data=json.dumps({'name': group.name})
    response = requests.post(url,
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        }
    )
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code in OK_STATUS_CODES:
        logger.info("Discord role successfully added")
        response = response.json()
        role = DiscordRole(role_id=response['id'], group=group)
        role.save()
    else:
        logger.error("Adding Disord role %s failed with %s : %s" % (group.name, response.status_code, response.json()))

def api_remove_discord_group(role):
    """
    Expects a DiscordRole object.
    Deletes the Discord Role from our database and the Discord server.
    """
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles/" + str(role.role_id)
    response = requests.delete(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code in OK_STATUS_CODES:
        role.delete()
    else:
        logger.error("Removing Disord role %s failed with %s" % (role.group.name, response.json()))

def api_add_user_to_discord_group(user, role):
    """
    Expects a User object and DiscordRole object.
    Adds the specified role to a user.
    """
    discord_id = DiscordToken.objects.get(user=user).userid
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  discord_id + "/roles/" + str(role.role_id)
    response = requests.put(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code in OK_STATUS_CODES:
        logger.info("Successfully added %s to %s... %s" % (user.username, role.group.name))
    else:
        logger.error("Adding %s to Discord role %s failed with %s" % (user.username, role.group.name, response.json()))

def api_remove_user_from_discord_group(user, role):
    """
    Expects a User object and DiscordRole object.
    Remove the specified role from a user.
    """
    discord_id = DiscordToken.objects.get(user=user).userid
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  discord_id + "/roles/" + str(role.role_id)
    response = requests.delete(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code in OK_STATUS_CODES:
        pass # OK
    else:
        logger.error("Removing %s from Discord role %s failed with %s" % (user.username, role.group.name, response.json()))
