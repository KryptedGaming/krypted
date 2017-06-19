from django.db import models
from django.contrib.auth.models import User, Group

class Game(models.Model):
    title = models.CharField(max_length=24, unique=True)
    leadership = models.ManyToManyField(User)
    source = models.URLField(max_length=256, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=24)
    text = models.CharField(max_length=500)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=1500, blank=True, null=True)
    points = models.IntegerField(default=0)
    games = models.ManyToManyField('Game')
    active = models.BooleanField(default=True)

    # Social
    twitter = models.URLField(max_length=32, blank=True, null=True)
    steam = models.URLField(max_length=256, blank=True, null=True)
    blizzard = models.CharField(max_length=32, blank=True, null=True)
    discord = models.CharField(max_length=32, blank=True, null=True)

    # Gaming

    def __str__(self):
        return self.user.username

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now=True)
    date_occuring = models.DateTimeField(auto_now=False)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128, blank=True, null=True)
    notes = models.CharField(max_length=32, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
