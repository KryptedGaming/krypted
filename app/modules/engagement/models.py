# DJANGO IMPORTS
from django.db import models
from django.contrib.auth.models import User
# EXTERNAL IMPORTS
from modules.guild.models import Guild
# MISC
import uuid

class Event(models.Model):
    """
    Event model for Krypted Authentication
    This model is used to create community events that can be tracked for participation
    Some notes:
        - null guild means community-wide event
        - null user means needs to be assigned
    """

    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    description = models.TextField()
    start_datetime = models.DateTimeField(auto_now=False)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, blank=True, null=True)

    # ATTENDENCE
    password = models.CharField(max_length=3)
    value = models.IntegerField(blank=True, null=True)
    registrants = models.ManyToManyField(User, blank=True, related_name="events_registered")
    participants = models.ManyToManyField(User, blank=True, related_name="events_participated")

    @property
    def is_expired(self):
        time_delta = self.start_datetime - datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if time_delta.total_seconds() < 3600:
            return True
        return False

    def get_absolute_url(self):
        return "/event/%s" % self.pk

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('manage_events', u'Can manage events'),
        )

class Survey(models.Model):
    """
    Survey model for Krypted Authentication. Used to wrap Google forms surveys
    sent out to the community or specific branches in the community
    """

    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    date_created = models.DateField(auto_now=True)
    date_finished = models.DateField()
    url = models.CharField(max_length=256)
    survey_key = models.UUIDField(default=uuid.uuid4)

    # REFERENCES
    users_started = models.ManyToManyField(User, blank=True, related_name='surveys_started')
    users_completed = models.ManyToManyField(User, blank=True, related_name='surveys_completed')

    @property
    def is_expired(self):
        if not self.date_finished:
            return False

        time_delta = self.date_finished - datetime.date.today()
        if time_delta.seconds < 0:
            return True
        return False
