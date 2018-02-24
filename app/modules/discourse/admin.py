from django.contrib import admin
from modules.discourse.models import *
# Register your models here.
@admin.register(DiscourseGroup)
class DiscourseGroupAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'get_group')

    def get_group(self, DiscourseGroup):
        return DiscourseGroup.group.name

@admin.register(DiscourseUser)
class DiscourseUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'get_user', 'all_groups')

    def get_user(self, DiscourseUser):
        return DiscourseUser.auth_user.username

    def all_groups(self, DiscourseUser):
        groups = []
        for group in DiscourseUser.groups.all():
            groups.append(group)
        return groups
