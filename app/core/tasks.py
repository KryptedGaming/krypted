from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS 
from django.contrib.auth.models import User, Group
from django.apps import apps
# LOCAL IMPORTS
from core.models import GroupIntegration
import logging, time

logger = logging.getLogger(__name__)
core_settings = apps.get_app_config('core')

"""
MAJOR TASKS
These tasks are periodically ran.
"""
@task()
def clear_inactive_users():
    for user in User.objects.all():
        if not user.info.discord or not user.info.discourse:
            clear_inactive_user.apply_async(args=[user.id])

@task()
def audit_eve_groups():
    eve_online_primary = GroupIntegration.objects.filter(type="EVE_ONLINE_PRIMARY").exists()
    eve_online_blue = GroupIntegration.objects.filter(type="EVE_ONLINE_BLUE").exists()
    for user in User.objects.all():
        audit_eve_groups_for_user.apply_async(args=[user.pk, eve_online_primary, eve_online_blue])

"""
MINOR TASKS
These tasks are used by the major tasks. 
"""
@task()
def clear_inactive_user(user_id):
    user = User.objects.get(id=user_id)
    for group in user.groups.all():
        user.groups.remove(group)
    for guild in user.guilds_in.all():
        guild.users.remove(user)

@task()
def audit_eve_groups_for_user(user_id, eve_online_primary_exists, eve_online_blue_exists):
    if not eve_online_primary_exists and not eve_online_blue_exists:
        logger.warning("Skipping EVE group audit for userid %s: MISSING_GROUP_INTEGRATIONS" % (user_id))
        return 
    if eve_online_primary_exists:
        primary_group = GroupIntegration.objects.get(type="EVE_ONLINE_PRIMARY").group 
    if eve_online_blue_exists:
        blue_group = GroupIntegration.objects.get(type="EVE_ONLINE_BLUE").group

    is_primary = False 
    is_blue = False 

    user = User.objects.get(id=user_id)
    eve_character = user.info.eve_character
    if eve_character:
        if eve_character.is_member():
            is_primary = True 
        if eve_character.is_blue():
            is_blue = True 
    
    if is_primary:
        if primary_group and primary_group not in user.groups.all():
            user.groups.add(primary_group)
    elif is_blue:
        if blue_group and blue_group not in user.groups.all():
            user.groups.add(blue_group)
    else:
        if primary_group and primary_group in user.groups.all():
            user.groups.remove(primary_group)
        if blue_group and blue_group in user.groups.all():
            user.groups.remove(blue_group)