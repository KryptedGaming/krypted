from django.contrib import admin
from modules.records.models import EventLog, GuildLog, SurveyLog

admin.site.register(EventLog)
admin.site.register(GuildLog)
admin.site.register(SurveyLog)
