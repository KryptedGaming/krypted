from django.db import models
from django.conf import settings
# external imports
from core.models import Guild

class UserStatistic(models.Model):
    # general statistics
    participation_points = models.DecimalField(default=0, decimal_places=2)
    # unique statistics
    event_points = models.DecimalField(default=0, decimal_places=2)
    survey_points = models.DecimalField(default=0, decimal_places=2)
    # references
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class StaffStatistic(models.Model):
    # general statistics
    participation_points = models.DecimalField(default=0, decimal_places=2)
    # unique statistics
    application_points = models.DecimalField(default=0, decimal_places=2)
    referral_points = models.DecimalField(default=0, decimal_places=2)
    # references
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class GuildStatistic(models.Model):
    # general statistics
    participation_points = models.DecimalField(default=0, decimal_places=2)
    # unique statistics
    event_points = models.DecimalField(default=0, decimal_places=2)
    survey_points = models.DecimalField(default=0, decimal_places=2)
    # references
    guild = models.OneToOneField(Guild, on_delete=models.CASCADE)
