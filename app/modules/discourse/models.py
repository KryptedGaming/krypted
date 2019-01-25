# DJANGO IMPORTS
from django.db import models
from django.contrib.auth.models import User, Group
# MISC
import logging
logger = logging.getLogger(__name__)

class DiscourseUser(models.Model):
    external_id = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="discourse_user")
    groups = models.ManyToManyField('DiscourseGroup')

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "None"

class DiscourseGroup(models.Model):
    external_id = models.BigIntegerField(blank=True, null=True)
    group = models.OneToOneField(Group, null=True, on_delete=models.SET_NULL, related_name="discourse_group")

    def __str__(self):
        if self.group:
            return self.group.name
        else:
            return "None"
