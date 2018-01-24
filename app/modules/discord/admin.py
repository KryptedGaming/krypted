from django.contrib import admin
from modules.discord.models import DiscordToken, DiscordRole

@admin.register(DiscordToken)
class DiscordTokenAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'user')

    def get_username(self, DiscordToken):
        return DiscordToken.user.username

@admin.register(DiscordRole)
class DiscordRoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'group_name')

    def group_name(self, DiscordToken):
        return DiscordToken.group.name
