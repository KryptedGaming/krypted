from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=24, unique=True)
    leadership = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=24)
    text = models.CharField(max_length=500)
    game = models.ForeignKey('Game', on_delete=models.CASCADE,
            blank=True, null=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=1500, blank=True, null=True)
    games = models.ManyToManyField('Game')
    active = models.BooleanField(default=True)
    pinned_games = models.ManyToManyField('Game', related_name="pinned", blank=True, null=True)

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
    description = models.CharField(max_length=128)
    notes = models.CharField(max_length=32)
