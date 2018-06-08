from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discord.models import DiscordUser, DiscordGroup
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.exceptions import RateLimitException
import logging, requests, json

logger = logging.getLogger(__name__)

@task()
def sync_discord_user(user_id):
    user = User.objects.get(id=user_id)
    if DiscordUser.objects.filter(user=user).exists():
        try:
            discord_user = DiscordUser.objects.get(user=user)
            call_counter = 0
            for discord_group in DiscordGroup.objects.all():
                if discord_group.group in user.groups.all() and discord_group not in discord_user.groups.all():
                    logger.info("%s has group %s, but was missing it. Syncing." % (user.username, discord_group.group.name))
                    add_user_to_discord_group.apply_async(args=[user.pk, discord_group.id], countdown=call_counter)
                    call_counter += 1
                if discord_group.group not in user.groups.all() and discord_group in discord_user.groups.all():
                    logger.info("%s does not have group %s, but had it. Syncing." % (user.username, discord_group.group.name))
                    remove_user_from_discord_group.apply_async(args=[user.pk, discord_group.id], countdown=call_counter)
                    call_counter += 1
        except Exception as e:
            logger.info("Failed to sync Discord user. %s" % e)



@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_discord_group(self, group):
    logger.info("[TASK] Adding Discord group: %s" % group)
    group = Group.objects.get(pk=group)
    DiscordGroup(group=group).save()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_discord_group(self, group):
    logger.info("[TASK] Removing Discord group: %s" % group)
    discord_group = DiscordGroup.objects.get(group__pk=group)
    discord_group.delete()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_user_to_discord_group(self, user, group):
    discord_user = DiscordUser.objects.get(user__pk=user)
    group = DiscordGroup.objects.get(id=group)
    logger.info("[TASK][DISCORD] Adding %s to Discord Group: %s" % (discord_user.user.username, group.group.name))
    discord_user.add_group(group)

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_user_from_discord_group(self, user, group):
    discord_user = DiscordUser.objects.get(user__pk=user)
    group = DiscordGroup.objects.get(id=group)
    logger.info("[TASK][DISCORD] Removing %s from Discord Group: %s" % (discord_user.user.username, group.group.name))
    discord_user.remove_group(group)
