from django.contrib import admin
from core.models import *

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

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('title', 'leadership_all')

    def leadership_all(self, guild):
        leader_list = []
        for leader in guild.leadership.all():
            leader_list.append(leader.username)
        return leader_list


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'group')

@admin.register(GroupRequest)
class GroupRequestAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_group', 'date_requested')

    def get_user(self):
        return self.user.username

    def get_group(self):
        return self.group.group.name

@admin.register(GroupEntity)
class GroupEntityAdmin(admin.ModelAdmin):
    list_display = ('get_group', 'hidden')

    def get_group(self, group_entity):
        return group_entity.group.name
