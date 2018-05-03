from django.contrib import admin
from modules.discord.models import DiscordUser, DiscordGroup

@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user')

    def get_username(self, DiscordUser):
        return DiscordUser.user.username

@admin.register(DiscordGroup)
class DiscordGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')

    def group_name(self, DiscordUser):
        return DiscordUser.group.name
