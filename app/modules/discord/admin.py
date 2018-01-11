from django.contrib import admin
from modules.discord.models import DiscordToken

@admin.register(DiscordToken)
class DiscordTokenAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'user')

    def get_username(self, DiscordToken):
        return DiscordToken.user.username
