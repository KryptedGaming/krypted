from django.contrib import admin
from modules.discourse.models import *
# Register your models here.
@admin.register(DiscourseGroup)
class DiscourseGroupAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'get_group')

    def get_group(self, DiscordToken):
        return DiscordToken.group.name
