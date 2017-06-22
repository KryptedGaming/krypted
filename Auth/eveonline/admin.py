from django.contrib import admin
from eveonline.models import Token

# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'access_token')

    def get_username(self, Token):
        return Token.user.username
