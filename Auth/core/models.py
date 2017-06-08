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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games = models.ManyToManyField('Game')
    active = models.BooleanField(default=True)
    pinned_games = models.ManyToManyField('Game', related_name="pinned")

    def __str__(self):
        return self.user.username
