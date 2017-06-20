from django.contrib import admin
from core.models import Notification, Profile, Game, Event

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_username')

    def get_username(self, notification):
        return notification.user.username

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'all_games', 'active')

    def all_games(self, profile):
        game_list = []
        for game in profile.games.all():
            game_list.append(game)
        return game_list

    def get_username(self, profile):
        return profile.user.username

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'leadership_all')

    def leadership_all(self, game):
        leader_list = []
        for leader in game.leadership.all():
            leader_list.append(leader.username)
        return leader_list

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'group')
