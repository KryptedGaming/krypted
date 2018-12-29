from __future__ import absolute_import, unicode_literals
# LOCAL IMPORTS
from modules.records.models import EventLog
# EXTERNAL IMPORTS
from celery import task
# MISC
import logging

logger = logging.getLogger(__name__)

@task()
def process_event_logs():
    # if no event logs, return
    if EventLog.objects.filter(type="participation").count() == 0:
        logger.info("No event logs to process, returning.")
        return
    # process event logs
    event_participation_logs = EventLog.objects.filter(type="participation").order_by('user')
    # pull first instance of user
    event_user_statistic = UserStatistic.objects.get_or_create(user=event_participation_logs[0].user)
    for event_participation_log in event_participation_logs:
        process_event_log.apply_async(args=[event_log_pk])
        # pull user statistic only when user changes
        if event_user != event_participation_log.user:
            event_user_statistic = UserStatistic.objects.get_or_create(user=event_participation_log.user)
        # consume event log
        event_user_statistic.event_points += 1
        event_registration_log = EventLog.objects.filter(event=event_participation_log.event, user=event_participation_log.user)
        # add additional points if registered
        if event_registration_log:
            event_user_statistic.event_points += 0.25
        # save user
        event_user_statistic.save()
        # delete logs
        event_participation_log.delete()
        if event_registration_log:
            event_registration_log.delete()

@task()
def process_event_log(event_log_pk):
    pass
