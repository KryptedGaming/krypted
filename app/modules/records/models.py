from django.db import models
from core.models import User, Event, Guild, Survey

# Create your models here.
class EventLog(models.Model):
    event_log_choices = (
        ("participation", "Participation"),
        ("registration", "Registration")
    )
    type = models.CharField(max_length=32, choices=event_log_choices)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class GuildLog(models.Model):
    guild_log_choices = (
        ("add_user", "Add User"),
        ("remove_user", "Remove User")
    )
    type = models.CharField(max_length=32, choices=guild_log_choices)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class StatisticLog(models.Model):
    statistic_log_choices = (
        ("event_log", "Event Logs"),
    )
    type = models.CharField(max_length=32, choices=statistic_log_choices, unique=True)
    datetime = models.DateTimeField(auto_now=True)

class SurveyLog(models.Model):
    event_log_choices = (
        ("started_survey","Started Survey"),
        ("completed_survey","Completed Survey"),
    )
    type = models.CharField(max_length=32, choices=event_log_choices)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
