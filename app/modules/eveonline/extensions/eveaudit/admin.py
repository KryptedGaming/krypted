from django.contrib import admin
from modules.eveonline.extensions.eveaudit.models import EveCharacterData

@admin.register(EveCharacterData)
class EveCharacterdata(admin.ModelAdmin):
    list_display = ['get_character_name']
    def get_character_name(self, EveCharacterData):
        return EveCharacterData.character.character_name
