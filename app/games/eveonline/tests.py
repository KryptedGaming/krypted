from django.test import TestCase
from games.eveonline.views.eve import *

# Create your tests here.
def character_mails_test():
    from games.eveonline.views.eve import get_character_data
    from games.eveonline.models import Token
    from django.conf import settings
    token = Token.objects.get(character_name="Porowns")
    data = get_character_data(settings.ESI_APP, token, settings.ESI_CLIENT)
    clean_character_mails(data)
    return data
