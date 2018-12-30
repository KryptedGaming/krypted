from __future__ import absolute_import, unicode_literals
# LOCAL IMPORTS
from modules.stats.models import StatisticModule, UserStatistic
# EXTERNAL IMPORTS
from celery import task
from modules.records.models import EventLog, StatisticLog
# MISC
import logging, datetime

logger = logging.getLogger(__name__)

@task()
def process_event_logs():
    # if no event logs, return
    if EventLog.objects.filter(type="participation").count() == 0:
        logger.info("No event logs to process, returning.")
        return
    # if processed previously, only pull eventlogs after date
    statistic_log = StatisticLog.objects.filter(type="event_log").first()
    if statistic_log:
        event_participation_logs = EventLog.objects.filter(
            type="participation",
            datetime__gte=statistic_log.datetime
            ).order_by('user')
    else:
        event_participation_logs = EventLog.objects.filter(
            `type="participation"
            ).order_by('user')
    # pull first instance of user
    for event_participation_log in event_participation_logs:
        process_event_log.apply_async(args=[event_log_pk])

@task()
def process_event_log(event_participation_log_pk):
    # get event log
    event_participation_log = EventLog.objects.get(pk=event_log_pk)
    # pull user statistic
    event_user_statistic = UserStatistic.objects.get_or_create(
        user=event_participation_logs[0].user
    )
    # pull guild statistic
    if event_log.event.guild:
        event_guild_statistic = GuildStatistic.objects.get_or_create(
            guild=event_log.event.guild
        )
    else:
        event_guild_statistic = None
    # process event log for user
    event_user_statistic.event_points += 1
    event_registration_log = EventLog.objects.filter(
        type="Registration",
        event=event_participation_log.event,
        user=event_participation_log.user
        )
    # add additional points if registered
    if event_registration_log:
        event_user_statistic.event_points += 0.25
    # save user
    event_user_statistic.save()
    # process event log for guild
    if event_guild_statistic:
        event_guild_statistic.event_points += 1
