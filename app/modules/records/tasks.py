from __future__ import absolute_import, unicode_literals
# DJANGO IMPORTS
from django.contrib.auth.models import User
# LOCAL IMPORTS
from modules.records.models import *
# EXTERNAL IMPORTS
from modules.engagement.models import Event
# MISC
from celery import task
import logging

logger = logging.getLogger(__name__)

@task()
def record_event_registration(event_id, user_id):
    user = User.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    EventLog(type="registration", user=user, event=event).save()

@task()
def record_event_participation(event_id, user_id):
    user = User.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    EventLog(type="participation", user=user, event=event).save()

@task()
def record_guild_join(event_id, user_id):
    pass

@task()
def record_guild_leave(event_id, user_id):
    pass
