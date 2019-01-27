# DJANGO IMPORTS
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
# LOCAL IMPORTS
from modules.records.models import EventLog, GuildLog
from modules.records.tasks import *
# EXTERNAL IMPORTS
from modules.engagement.models import Event

import logging
logger = logging.getLogger(__name__)

# TODO: Should these be implemented in core? 
@receiver(m2m_changed, sender=Event.participants.through)
def event_participants_change(sender, **kwargs):
    event = kwargs.get('instance')
    action = str(kwargs.get('action'))
    users = []
    for pk in kwargs.get('pk_set'):
        users.append(pk)
    if action == "post_remove":
        for user in users:
            if EventLog.objects.filter(user__pk=user, event=event).exists():
                logger.info("Deleting existing participation EventLog for %s(user_id_%s)" % (event.name, user))
                EventLog.objects.get(user__pk=user, event=event, type="participation").delete()
    elif action == "post_add":
        for user in users:
            logger.info("Adding participation EventLog for %s(user_id_%s)" % (event.name, user))
            record_event_participation.apply_async(args=[event.pk, user])

@receiver(m2m_changed, sender=Event.registrants.through)
def event_registrants_change(sender, **kwargs):
    event = kwargs.get('instance')
    action = str(kwargs.get('action'))
    users = []
    for pk in kwargs.get('pk_set'):
        users.append(pk)
    if action == "post_remove":
        for user in users:
            if EventLog.objects.filter(user__pk=user, event=event).exists():
                logger.info("Deleting existing registration EventLog for %s(user_id_%s)" % (event.name, user))
                EventLog.objects.get(user__pk=user, event=event, type="registration").delete()
    elif action == "post_add":
        for user in users:
            logger.info("Adding registration EventLog for %s(user_id_%s)" % (event.name, user))
            record_event_registration.apply_async(args=[event.pk, user])
