from django.contrib import admin
from modules.eveonline.models import *

# Register your models here.
@admin.register(EveToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'expiry')

@admin.register(EveCharacter)
class EveCharacterAdmin(admin.ModelAdmin):
    search_fields = ['character_name']
    list_display = ('character_name', 'get_username')

    def get_username(self, EveCharacter):
        if EveCharacter.user:
            return EveCharacter.user.username
        else:
            return None

@admin.register(EveCorporation)
class EveCorporationAdmin(admin.ModelAdmin):
    list_display = ('name', 'ceo')
