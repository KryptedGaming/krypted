from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from modules.eveonline.models import EveCorporation, EveCharacter
from esipy import EsiApp, App
import json, logging

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

class EveClient:
    def __init__(self):
        self.ESI_APP = EsiApp().get_latest_swagger

    def get_character(self, character_id):
        # get character
        op = self.ESI_APP.op['get_characters_character_id'](character_id=character_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # add portrait data
        op = self.ESI_APP.op['get_characters_character_id_portrait'](character_id=character_id)
        portrait = eve_settings.ESI_CLIENT.request(op)
        response.data['portrait'] = portrait.data['px64x64'].replace("http", "https")
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def get_corporation(self, corporation_id):
        op = self.ESI_APP.op['get_corporations_corporation_id'](corporation_id=corporation_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def get_alliance(self, alliance_id):
        op = self.ESI_APP.op['get_alliances_alliance_id'](alliance_id=alliance_id)
        response = eve_settings.ESI_CLIENT.request(op)
        # clean up cluttered data
        if 'description' in response.data:
            response.data.pop('description', None)
        return response

    def resolve_ids(self, ids):
        op = self.ESI_APP.op['post_universe_names'](ids=ids)
        response = eve_settings.ESI_CLIENT.request(op)
        return response

    def get_corporation_characters(self, corporation_id):
        corporation = EveCorporation.objects.get(corporation_id=corporation_id)
        eve_character = EveCharacter.objects.filter(corporation=corporation).first()
        eve_character.token.refresh()
        eve_settings.ESI_SECURITY.update_token(eve_character.token.populate())
        op = self.ESI_APP.op['get_corporations_corporation_id_members'](corporation_id=corporation_id)
        response = eve_settings.ESI_CLIENT.request(op)
        return response.data

    def get_character_skills(self, character_id):

        if (not self.update_esi_security(character_id)):
            return None
        
        logger.info("Retrieving skills for EVE character: %s" % character_id)

        op = self.ESI_APP.op['get_characters_character_id_skills'](
            character_id=character_id)
        
        response = eve_settings.ESI_CLIENT.request(op)

        if response.status == 200:
            logger.info('Successfully retrieved skills for EVE Character: %s' % character_id)
            # convert response format to something more useful
            parsed_data = {}
            for skill in response.data['skills']:
                parsed_data[str(skill['skill_id'])] = {
                    "skill_level": skill['active_skill_level'],
                    "skill_points": skill['skillpoints_in_skill']
                }
            
            # map skills to categories
            import os.path
            import modules.eveonline 
            path = os.path.dirname(modules.eveonline.__file__)
            with open('%s/dumps/skills.json' % path, 'r') as file:
                skills=json.load(file)
            for category in skills:
                print(category)
                for skill in skills[category]:
                    print(skill)
                    if skill in parsed_data.keys():
                        skills[category][skill]["skill_points"] = parsed_data[skill]['skill_points']
                        skills[category][skill]["skill_level"] = parsed_data[skill]['skill_level']                        
            return skills
        else:
            logger.warning("Bad response retrieving skills for %s" % character_id)
            logger.warning("%s" % response.status)
            return None
    
    def get_character_mails(self, character_id):
        if (not self.update_esi_security(character_id)):
            return None

        logger.info("Retrieving mail for EVE character: %s" % character_id)

        op = self.ESI_APP.op['get_characters_character_id_mail'](
            character_id=character_id)
        
        response = eve_settings.ESI_CLIENT.request(op)

        if response.status == 200:
            character_ids = set()
            # first pass, clean datas and pull ids
            for mail in response.data:
                # pull character IDs
                if int(mail['from']) < 145000000 or mail['from'] > 146000000:
                    character_ids.add(mail['from'])
                for recipient in mail['recipients']:
                    if recipient['recipient_type'] != "mailing_list":
                        character_ids.add(recipient['recipient_id'])
                # clean timestamps
                time = str(mail['timestamp']).split("T")[0]
                mail['timestamp'] = time
                # add data 
                # TODO: Refactor and move to an EveClient() method
                op = self.ESI_APP.op['get_characters_character_id_mail_mail_id'](character_id=character_id, mail_id=mail['mail_id'])
                mail_body = eve_settings.ESI_CLIENT.request(op).data
                if 'body' in mail_body:
                    mail['body'] = mail_body['body']
                else:
                    mail['body'] = "Unable to pull mail body."
            # resolve character IDs to names 
            character_ids = self.resolve_ids(list(character_ids)).data
            # convert to dict
            resolved_character_ids = {str(character['id']):character for character in character_ids}
            # second pass, replace IDs
            for mail in response.data:
                response_character_id = str(mail['from'])
                if response_character_id in resolved_character_ids:
                    mail['from'] = resolved_character_ids[response_character_id]['name']
                for recipient in mail['recipients']:
                    recipient_character = str(recipient['recipient_id'])
                    if recipient_character in resolved_character_ids:
                        recipient['recipient_id'] = resolved_character_ids[recipient_character]['name']
                        if recipient['recipient_type'] == "character":
                            recipient['recipient_url'] = "https://evewho.com/pilot/" + recipient['recipient_id'].replace(" ", "+")
                        elif recipient['recipient_type'] == "corporation":
                            recipient['recipient_url'] = "https://evewho.com/corp/" + recipient['recipient_id'].replace(" ", "+")
                        elif recipient['recipient_type'] == "alliance":
                            recipient['recipient_url'] = "https://evewho.com/alli/" + recipient['recipient_id'].replace(" ", "+")
                        else:
                            recipient['recipient_url'] = ""
            return response.data
        else:
            logger.warning("Bad response retrieving mail for %s" % character_id)
            logger.warning("%s" % response.status)
            return None

    def get_character_journal(self, character_id):
        if (not self.update_esi_security(character_id)):
            return None 

        logger.info("Retrieving journal for EVE character: %s" % character_id)

        op = self.ESI_APP.op['get_characters_character_id_wallet_journal'](
            character_id=character_id)
        
        response = eve_settings.ESI_CLIENT.request(op)

        if (response.status == 200):
            character_ids = []
            # collect character IDs
            for entry in response.data:
                if 'first_party_id' in entry:
                    character_ids.append(entry['first_party_id'])
                if 'second_party_id' in entry:
                    character_ids.append(entry['second_party_id'])
            # return None if no entries
            if (not character_ids):
                return None 
            # resolve character IDs
            resolved_character_ids = self.resolve_ids(character_ids).data
            # convert to dict
            resolved_character_ids = {str(character['id']):character for character in resolved_character_ids}
            # add resolved character IDs
            for entry in response.data:
                if 'first_party_id' in entry:
                    character_id = str(entry['first_party_id'])
                    entry['first_party_id'] = resolved_character_ids[character_id]['name']
                if 'second_party_id' in entry:
                    character_id = str(entry['second_party_id'])
                    entry['second_party_id'] = resolved_character_ids[character_id]['name']

            return response.data
        else: 
            logger.warning("Bad response retrieving journal for %s" % character_id)
            logger.warning("%s" % response.status)
            return None
        
    def get_character_contracts(self, character_id):
        return None
    
    def get_character_contacts(self, character_id):
        return None 
    
    def get_character_assets(self, character_id):
        pass
    # HELPERS
    def update_esi_security(self, character_id):
        try:
            token = EveCharacter.objects.get(character_id=character_id).token
        except ObjectDoesNotExist:
            logger.warning("Attempted to update EsiSecurity for unregistered character: %s" % character_id)
            return False

        # refresh eve token
        token.refresh()
        # populate ESIApp() with character token
        eve_settings.ESI_SECURITY.update_token(token.populate())
        return True


