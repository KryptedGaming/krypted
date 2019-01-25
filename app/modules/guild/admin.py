from django.contrib import admin
from modules.guild.models import *

admin.site.register(Guild)
admin.site.register(GuildApplicationTemplate)
admin.site.register(GuildApplicationQuestion)
admin.site.register(GuildApplicationResponse)
admin.site.register(GuildApplication)
