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

"""
MINOR TASKS
These tasks are used by the major tasks. 
"""
@task()
def clear_inactive_user(user_id):
    user = User.objects.get(id=user_id)
    for group in user.groups.all():
        user.groups.remove(group)