from app.conf import eve as eve_settings
from games.eveonline.models import EveCorporation, EveCharacter
import json

class EveClient:
    # def get_character(character_id):
    #     if EveCharacter.objects.filter(character_id=character_id).exists():
    #         return EveCharacter.objects.get(character_id=character_id)
    #     else:
    #         op = eve_settings.ESI_APP.op['get_characters_character_id'](character_id=character_id)
    #         response = eve_settings.ESI_CLIENT.request(op)
    #         op = eve_settings.ESI_APP.op['get_characters_character_id_portrait'](character_id=character_id)
    #         portrait = eve_settings.ESI_CLIENT.request(op)
    #         character = EveCharacter(
    #                 character_id=character_id,
    #                 character_name=response.data['name'],
    #                 character_portrait=portrait.data['px64x64'].replace("http", "https"),
    #                 main=None,
    #                 token=None,
    #                 user=None
    #         )
    #         character.save()
    #         return EveCharacter.objects.get(character_id=character_id)

    def get_corporation_characters(corporation_id):
        corporation = EveCorporation.objects.get(corporation_id=corporation_id)
        eve_character = EveCharacter.objects.filter(corporation=corporation).first()
        eve_character.token.refresh()
        eve_settings.ESI_SECURITY.update_token(eve_character.token.populate())
        op = eve_settings.ESI_APP.op['get_corporations_corporation_id_members'](corporation_id=corporation_id)
        response = eve_settings.ESI_CLIENT.request(op)
        return response.data
