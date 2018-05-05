from django.shortcuts import render, redirect
from games.eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Guild
from core.decorators import login_required, tutorial_complete
from core.views.base import get_global_context
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from operator import itemgetter
import json, logging, datetime

logger = logging.getLogger(__name__)
"""
Helper Functions
Used for the above web calls
"""
def get_raw_character_data(token):
    logger.info("Starting EVE Online Audit for Character: %s" % token.character_name)
    token.refresh()
    settings.ESI_SECURITY.update_token(token.populate())
    name_scopes = {
                   'mails': 'get_characters_character_id_mail',
                   'skills': 'get_characters_character_id_skills',
                   'transactions': 'get_characters_character_id_wallet_transactions',
                   'journal': 'get_characters_character_id_wallet_journal',
                   'contacts': 'get_characters_character_id_contacts',
                   'assets': 'get_characters_character_id_assets',
                   'orders': 'get_characters_character_id_orders',
                   'notifications': 'get_characters_character_id_notifications',
                   'contracts': 'get_characters_character_id_contracts',
                   'wallet': 'get_characters_character_id_wallet'
                   }
    data = {}
    data['character_id'] = token.character_id
    for scope in name_scopes:
        op = settings.ESI_APP.op[name_scopes[scope]](character_id=token.character_id)
        response = settings.ESI_CLIENT.request(op)
        if response.status == 200:
            data[scope] = response.data
        else:
            print("Bad response: %s" % response.status)

    if data['journal']:
        data = clean_character_journal(data)
    if data['mails']:
        data = clean_mail_results(data)
    if data['contracts']:
        data = clean_contracts(data)
    if data['contacts']:
        data = clean_contacts(data)

    return data

def clean_character_journal(data):
    query = []
    journal = data['journal']
    if journal:
        for entry in journal:
            query.append(entry.first_party_id)
            query.append(entry.second_party_id)
        op = settings.ESI_APP.op['post_universe_names'](ids=query)
        response = settings.ESI_CLIENT.request(op)
        print(response.status)
        if response.status == 200:
            counter1 = 0
            counter2 = 0
            for value in response.data:
                counter1 += 1
                for entry in journal:
                    counter2 += 2
                    try:
                        if entry.first_party_id == value.id:
                            entry.first_party_id = value.name
                        elif entry.second_party_id == value.id:
                            entry.second_party_id = value.name
                    except:
                        entry['first_party_id'] = None
                        entry['second_party_id'] = None
    return data


def clean_mail_results(data):
    # Clean up mail player ids
    character_ids = set()
    for mail in data['mails']:
        character_ids.add(int(mail['from']))
        for recipient in mail['recipients']:
            if recipient['recipient_type'] != "mailing_list":
                character_ids.add(recipient['recipient_id'])
    character_ids = list(character_ids)
    op = settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = settings.ESI_CLIENT.request(op).data
    for character in character_ids:
        for mail in data['mails']:
            if mail['from'] == character['id']:
                mail['from'] = character['name']
            for recipient in mail['recipients']:
                if recipient['recipient_id'] == character['id']:
                    recipient['recipient_id'] = character['name']
    # Clean up mail dates
    for mail in data['mails']:
        time = str(mail['timestamp']).split("T")[0]
        mail['timestamp'] = time
    # Clean up recipicients
    for mail in data['mails']:
        character_ids = []
        for recipient in mail['recipients']:
            if recipient['recipient_type'] == "character":
                recipient['recipient_url'] = "https://evewho.com/pilot/" + recipient['recipient_id'].replace(" ", "+")
            elif recipient['recipient_type'] == "corporation":
                recipient['recipient_url'] = "https://evewho.com/corp/" + recipient['recipient_id'].replace(" ", "+")
            elif recipient['recipient_type'] == "alliance":
                recipient['recipient_url'] = "https://evewho.com/alli/" + recipient['recipient_id'].replace(" ", "+")
            else:
                recipient['recipient_url'] = ""
        # mail['recipients'] = ",".join(map(str,character_ids))
    # Add mail data
    for mail in data['mails']:
        op = settings.ESI_APP.op['get_characters_character_id_mail_mail_id'](character_id=data['character_id'], mail_id=mail['mail_id'])
        mail_body = settings.ESI_CLIENT.request(op).data
        mail['body'] = mail_body['body']
    return data

def clean_contacts(data):
    character_ids = []
    for contact in data['contacts']:
        character_ids.append(contact['contact_id'])
    op = settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = settings.ESI_CLIENT.request(op).data
    for character in character_ids:
        for contact in data['contacts']:
            if contact['contact_id'] == character.id:
                contact['contact_id'] = character.name
                # create evewho links
                if contact['contact_type'] == "character":
                    contact['contact_url'] = "https://evewho.com/pilot/" + contact['contact_id'].replace(" ", "+")
                elif contact['contact_type'] == "corporation":
                    contact['contact_url'] = "https://evewho.com/corp/" + contact['contact_id'].replace(" ", "+")
                elif contact['contact_type'] == "alliance":
                    contact['contact_url'] = "https://evewho.com/alli/" + contact['contact_id'].replace(" ", "+")

    data['contacts'] = sorted(data['contacts'], key=itemgetter('standing'))
    return data

def clean_contracts(data):
    character_ids = []
    for contract in data['contracts']:
        if contract['issuer_id'] != 0:
            character_ids.append(contract['issuer_id'])
        if contract['acceptor_id'] != 0:
            character_ids.append(contract['acceptor_id'])
    op = settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = settings.ESI_CLIENT.request(op).data
    print(character_ids)
    for character in character_ids:
        for contract in data['contracts']:
            if contract['issuer_id'] == character.id:
                contract['issuer_id'] = character.name
            elif contract['acceptor_id'] == character.id:
                contract['acceptor_id'] = character.name
    # Clean up mail dates
    for contract in data['contracts']:
        time = str(contract['date_issued']).split("T")[0]
        contract['timestamp'] = time

    return data
