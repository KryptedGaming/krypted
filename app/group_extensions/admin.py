from django.contrib import admin, messages
from .models import ExtendedGroup, GroupTrigger


@admin.register(ExtendedGroup)
class ExtendedGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'type')
    search_fields = ('group', 'type')


@admin.register(GroupTrigger)
class GroupTriggerAdmin(admin.ModelAdmin):
    list_display = ('trigger_group', 'add_groups_on_trigger',
                    'remove_groups_on_trigger')
    search_fields = ('trigger_group',)
