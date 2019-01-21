from django.db import models
from core.models import User, Event, Guild

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
