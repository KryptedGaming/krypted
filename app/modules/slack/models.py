from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class SlackUser(models.Model):
    slack_id = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class SlackChannel(models.Model):
    slack_id = models.CharField(max_length=64)
    groups = models.ManyToManyField(Group, null=True, blank=True)
