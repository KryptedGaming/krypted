from __future__ import absolute_import, unicode_literals
from celery import task
# DJANGO IMPORTS
from django.apps import apps
from django.db.models import Q
# INTERNAL IMPORTS
from modules.eveonline.models import EveCharacter
from modules.eveonline.client import EveClient
from modules.eveonline.extensions.eveaudit.models import EveCharacterData
# MISC
from esipy import App
import logging, time, datetime, pytz

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

"""
MAJOR TASKS
These tasks are periodically ran.
"""

@task()
def update_eve_characters_data():
    for character in EveCharacter.objects.filter(~Q(token=None)):
        if character.is_member() or character.is_blue():
            update_character_data.apply_async(args=[character.character_id], countdown=60*(character.pk % 100))

@task()
def update_eve_character_skills():
    for character in EveCharacter.objects.filter(~Q(token=None)):
        if character.is_member() or character.is_blue():
                update_character_skills.apply_async(args=[character.character_id])

# HELPER TASKS
@task()
def update_character_data(character_id):
    eve_client = EveClient()
    eve_character = EveCharacter.objects.get(character_id=character_id)
    logger.info("Updating Character Data for %s")
    eve_character_data = EveCharacterData.objects.get_or_create(character=eve_character)[0]
    # update skillpoints
    skillpoints = EveClient().get_character_skill_points(character_id)
    if skillpoints:
        eve_character_data.total_skillpoints = skillpoints
    # update wallet balance
    balance = EveClient().get_character_wallet_balance(character_id)
    if balance:
        eve_character_data.total_isk = balance
    # update contracts
    contracts = EveClient().get_character_contracts(character_id)
    if contracts:
        eve_character_data.contracts = contracts
    # update skill tree 
    skill_tree = EveClient().get_character_skill_tree(character_id)
    if skill_tree:
        eve_character_data.skill_tree = skill_tree
    # update journal 
    journal = EveClient().get_character_journal(character_id)
    if journal:
        eve_character_data.journal = journal
    # update contacts
    contacts = EveClient().get_character_contacts(character_id)
    if contacts:
        eve_character_data.contacts = contacts
    # update mails 
    mails = EveClient().get_character_mails(character_id)
    if mails:
        eve_character_data.mails = mails
    # update hangar assets
    hangar_assets = EveClient().get_character_hangar_assets(character_id)
    if hangar_assets:
        eve_character_data.assets = hangar_assets

    eve_character_data.save()
    
@task()
def update_character_skills(character_id):
    eve_character_data = EveCharacter.objects.get(character_id=character_id).data
    logger.info("Updating Character skills for %s")
    skills = {}
    for category in eve_character_data.skill_tree:
        for skill in eve_character_data.skill_tree[category]:
            skill_object = eve_character_data.skill_tree[category][skill]
            try:
                skills[skill_object['name']] = {
                    'skill_points': skill_object['skill_points'],
                    'skill_level': skill_object['skill_level']
                }
                logger.debug("Adding skill: %s" % skill_object['name'])
            except Exception as e:
                logger.debug("Skipping skill: %s" % skill_object['name'])
    eve_character_data.skills = skills 
    eve_character_data.save()
