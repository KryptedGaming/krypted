from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from core.models import *

admin.site.unregister(DjangoGroup)
admin.site.register(User, UserAdmin)

admin.site.register(Group, GroupAdmin)
admin.site.register(Event)
admin.site.register(Survey)
admin.site.register(Guild)
admin.site.register(GroupRequest)
admin.site.register(GuildApplicationTemplate)
admin.site.register(GuildApplicationQuestion)
admin.site.register(GuildApplicationResponse)
admin.site.register(GuildApplication)
