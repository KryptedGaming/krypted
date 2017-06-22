from django.contrib import admin
from eveonline.models import Token, EveCharacter

# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'access_token')

@admin.register(EveCharacter)
class EveCharacterAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'user')

    def get_username(self, EveCharacter):
        return EveCharacter.user.username
