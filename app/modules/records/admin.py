from django.contrib import admin
from modules.records.models import EventLog, GuildLog

admin.site.register(EventLog)
admin.site.register(GuildLog)
