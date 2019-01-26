from __future__ import absolute_import, unicode_literals
# DJANGO IMPORTS
from django.contrib.auth.models import User, Group
# INTERNAL IMPORTS
from modules.discord.models import DiscordUser, DiscordGroup, DiscordChannel
from modules.discord.client import DiscordClient
# MISC
from celery import task
import logging

logger = logging.getLogger(__name__)

@task()
def sync_discord_users():
    pass

@task()
def sync_discord_user(user_id):
    user = User.objects.get(pk=user_id)
    discord_user = DiscordUser.objects.get(user=user)
    for discord_group in discord_user.groups.all():
        if discord_group.group not in user.groups.all():
            remove_user_from_discord_group.apply_async(args=[user_id, discord_group.group.pk])

@task()
def update_discord_users():
    for user in User.objects.all():
        update_discord_user.apply_async(args=[user.id], countdown=user.id)

@task()
def update_discord_user(user_id):
    # pull objects from database
    user = User.objects.get(pk=user_id)
    # break if not discord
    if not user.discord:
        return None
    # call client
    response = DiscordClient.get_discord_user(user.discord.external_id)
    # update username
    if response.status_code == 200:
        discord = user.discord
        if response.json()['nick'] != None:
            discord.username = response.json()['nick'] + "#" + response.json()['user']['discriminator']
            discord.save()
        else:
            discord.username = response.json()['user']['username'] + "#" + response.json()['user']['discriminator']
            discord.save()
    else:
        if 'code' in response.json():
            if response.json()['code'] == 10007:
                discord = user.discord
                discord.delete()

@task(rate_limit="1/s")
def send_discord_message(channel, message, **kwargs):
    if kwargs.get('user'):
        discord_user=DiscordUser.objects.get(user__id=kwargs.get('user'))
        message = message + " <@%s>" % discord_user.external_id
    elif kwargs.get('group'):
        discord_group=DiscordGroup.objects.get(group__id=kwargs.get('group'))
        message = message + " <@&%s>" % discord_group.external_id
    else:
        message = message
    response = DiscordClient.send_message(channel, message)
    # TODO: Handle response

@task(bind=True, rate_limit="1/s")
def add_discord_group(self, group_id):
    # Pull objects from database
    group = Group.objects.get(id=group_id)
    # Check if exists
    if DiscordGroup.objects.filter(group=group).exists():
        return True
    # Call discord client
    response = DiscordClient.add_group_to_discord_server(group.name)
    # Handle response
    try:
        if response.status_code == 429:
            # RATE LIMIT
            logger.warning("RATELIMIT - Adding Group [%s] to Discord Server." % group.name)
            self.apply_async(args=[group.pk], cooldown=int(response.json()['retry_after'])/1000)
        elif response.status_code == 200:
            # SUCCESS
            logger.info("SUCCESS - Adding Group [%s] to Discord Server." % group.name)
            discord_group = DiscordGroup(
                external_id=response.json()['id'],
                group=group,
            )
            discord_group.save()
        else:
            # FAILURE
            logger.error("FAILURE - Adding Group [%s] to Discord Server: %s" % (group.name, response.json()))
    except Exception as e:
        # FATAL
        logger.error("FATAL - Error with add_discord_group function. %s" % e)

@task(bind=True, rate_limit="1/s")
def remove_discord_group(self, discord_group_external_id):
    discord_group = DiscordGroup.objects.get(external_id=discord_group_external_id)
    # Call discord client
    response = DiscordClient.remove_group_from_discord_server(discord_group_external_id)
    # Handle response
    try:
        if response.status_code == 429:
            # RATE LIMIT
            logger.warning("RATELIMIT - Removing Group [%s] from Discord Server." % discord_group.external_id)
            self.apply_async(args=[discourse_group_external_id], countdown=int(response.json()['retry_after'])/1000)
        elif response.status_code == 204:
            # SUCCESS
            logger.info("SUCCESS - Removing Group [%s] from Discord Server." % discord_group.external_id)
            discord_group.delete()
        else:
            # FAILURE
            logger.error("FAILURE - Removing Group [%s] from Discord Server: %s" % (discord_group.external_id, response.json()))
    except Exception as e:
        # FATAL
        logger.error("FATAL - Error with remove_discord_group function. %s" % e)

@task(bind=True, rate_limit="1/s")
def add_user_to_discord_group(self, user_id, group_id):
    # Pull objects from database
    discord_user = DiscordUser.objects.get(user__id=user_id)
    discord_group = DiscordGroup.objects.get(group__id=group_id)
    # Call discord client
    response = DiscordClient.add_group_to_discord_user(discord_user.external_id, discord_group.external_id)
    # Handle response
    try:
        if response.status_code == 429:
            # RATE LIMIT
            logger.warning("RATELIMIT - Adding Group [%s] to User [%s]." % (discord_group.group.name, discord_user.username))
            self.apply_async(args=[user_id, group_id], countdown=int(response.json()['retry_after'])/1000)
        elif response.status_code == 204:
            # SUCCESS
            logger.info("SUCCESS - Adding Group [%s] to User [%s]." % (discord_group.group.name, discord_user.username))
            discord_user.groups.add(discord_group)
        else:
            # FAILURE
            logger.error("FAILURE - Adding Group [%s] to User [%s]." % (discord_group.group.name, discord_user.username))
    except Exception as e:
        # FATAL
        logger.error("FATAL - Error with add_group_to_discord_user function. %s" % e)

@task(bind=True, rate_limit="1/s")
def remove_user_from_discord_group(self, user_id, group_id):
    # Pull objects from the database
    discord_user = DiscordUser.objects.get(user__id=user_id)
    discord_group = DiscordGroup.objects.get(group__id=group_id)
    # Call discord client
    response = DiscordClient.remove_group_from_discord_user(discord_user.external_id, discord_group.external_id)
    # Handle response
    try:
        if response.status_code == 429:
            # RATE LIMIT
            logger.warning("RATELIMIT - Removing Group [%s] from [%s]." % (discord_group.group.name, discord_user.username))
            self.apply_async(args=[user_id, group_id], countdown=int(response.json()['retry_after'])/1000)
        elif response.status_code == 204:
            # SUCCESS
            logger.info("SUCCESS - Removing Group [%s] from [%s]" % (discord_group.group.name, discord_user.username))
            discord_user.groups.remove(discord_group)
        else:
            # FAILURE
            logger.error("FAILURE - Removing Group [%s] from [%s]" % (discord_group.group.name, discord_user.username))
    except Exception as e:
        # FATAL
        logger.error("FATAL - Error with remove_group_from_discord_user function. %s" % e)

@task(bind=True, rate_limit="1/s")
def send_discord_channel_message(self, discord_channel_name, message, **kwargs):
    # pull objects from db
    discord_channel = DiscordChannel.objects.get(name=discord_channel_name)
    # process message
    if kwargs.get('user'):
        discord_user=DiscordUser.objects.get(user__id=kwargs.get('user'))
        processed_message = message + " <@%s>" % discord_user.external_id
    elif kwargs.get('group'):
        discord_group=DiscordGroup.objects.get(group__id=kwargs.get('group'))
        processed_message = message + " <@&%s>" % discord_group.external_id
    else:
        processed_message = message
    # call discord client
    response = DiscordClient.send_channel_message(discord_channel.external_id, processed_message)
    try:
        if response.status_code == 429:
            logger.warning("RATELIMIT sending Discord message")
            self.apply_async(args=[discord_channel_name, message], kwargs=kwargs, countdown=int(response.json()['retry_after'])/1000)
    except:
        pass
