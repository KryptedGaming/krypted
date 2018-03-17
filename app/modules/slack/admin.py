from django.contrib import admin
from modules.slack.models import SlackUser

@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ('slack_id', 'get_user')

    def get_user(self, SlackUser):
        return SlackUser.user.username
