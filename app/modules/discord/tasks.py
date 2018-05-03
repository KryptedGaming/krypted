from __future__ import absolute_import, unicode_literals
from celery import task
from modules.discord.models import DiscordUser, DiscordGroup
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.exceptions import RateLimitException
import logging, requests, json

logger = logging.getLogger(__name__)

@task()
def sync_discord_user(user):
    user = DiscordUser.objects.get(user__pk=user)
    groups = Group.objects.all()
    for group in groups:
        discord_group = DiscordGroup.objects.get(group=group)
        logger.info(str(user.groups.all()))
        logger.info(str(user.user.groups.all()))
        if group in user.user.groups.all() and discord_group not in user.groups.all():
            logger.info("[TASK] User failed case ADD role check for %s" % (group.name))
            add_user_to_discord_group.apply_async(args=[str(user.user.pk), str(discord_group.id)])
        elif group not in user.user.groups.all() and discord_group in user.groups.all():
            logger.info("[TASK] User failed case REMOVE role check for %s" % (group.name))
            remove_user_from_discord_group.apply_async(args=[str(user.user.pk), str(discord_group.id)])
        else:
            logger.info("[TASK] User passed role check for %s" % (group.name))

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_discord_group(self, group):
    logger.info("[TASK] Adding Discord group: %s" % group)
    group = Group.objects.get(pk=group)
    DiscordGroup(group=group).save()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_discord_group(self, group):
    logger.info("[TASK] Removeing Discord group: %s" % group)
    discord_group = DiscordGroup.objects.get(group__pk=group)
    discord_group.delete()

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def add_user_to_discord_group(self, user, group):
    logger.info("[TASK] Adding %s to Discord Group: %s" % (user, group))
    discord_user = DiscordUser.objects.get(user__pk=user)
    group = DiscordGroup.objects.get(id=group)
    discord_user.add_group(group)

@task(bind=True, autoretry_for=(RateLimitException,), retry_backoff=True)
def remove_user_from_discord_group(self, user, group):
    logger.info("[TASK] Removing %s from Discord Group: %s" % (user, group))
    discord_user = DiscordUser.objects.get(user__pk=user)
    group = DiscordGroup.objects.get(id=group)
    discord_user.remove_group(group)
