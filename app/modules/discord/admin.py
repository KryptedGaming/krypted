from django.contrib import admin
from modules.discord.models import *

@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_username')
    search_fields = ['username', 'user__username']
    def get_username(self, DiscordUser):
        return DiscordUser.user.username
    # def get_eve_character(self, DiscordUser):
    #     return DiscordUser.user.eve_character

admin.site.register(DiscordGroup)
