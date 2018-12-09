from app.conf import eve as eve_settings
from games.eveonline.models import EveCorporation, EveCharacter
from esipy import App
import json

ESI_APP = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

class EveClient:
    def get_character(character_id):
        # get character
        op = ESI_APP.op['get_characters_character_id'](character_id=character_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # add portrait data
        op = ESI_APP.op['get_characters_character_id_portrait'](character_id=character_id)
        portrait = eve_settings.ESI_CLIENT.request(op)
        response.data['portrait'] = portrait.data['px64x64'].replace("http", "https")
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def get_corporation(corporation_id):
        op = ESI_APP.op['get_corporations_corporation_id'](corporation_id=corporation_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def get_alliance(alliance_id):
        op = ESI_APP.op['get_alliances_alliance_id'](alliance_id=alliance_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def resolve_ids(ids):
        op = ESI_APP.op['post_universe_names'](ids=ids)
        response = eve_settings.ESI_CLIENT.request(op)
        return response

    def get_corporation_characters(corporation_id):
        corporation = EveCorporation.objects.get(corporation_id=corporation_id)
        eve_character = EveCharacter.objects.filter(corporation=corporation).first()
        eve_character.token.refresh()
        eve_settings.ESI_SECURITY.update_token(eve_character.token.populate())
        op = ESI_APP.op['get_corporations_corporation_id_members'](corporation_id=corporation_id)
        response = eve_settings.ESI_CLIENT.request(op)
        return response.data
