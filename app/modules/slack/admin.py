from django.contrib import admin
from modules.slack.models import *

@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user')

    def get_user(self, SlackUser):
        return SlackUser.user.username

@admin.register(SlackChannel)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_groups')

    def get_groups(self, SlackChannel):
        groups = []
        for group in SlackChannel.groups.all():
            groups.append(group)
        return groups
