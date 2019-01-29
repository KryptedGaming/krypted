# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.apps import apps
# INTERNAL IMPORTS
from modules.eveonline.models import EveToken, EveCharacter
# EXTERNAL IMPORTS
from operator import itemgetter
import logging, time

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def dashboard(request):
    context = {}
    context['alt_types'] = eve_settings.EVE_ALT_TYPES
    logger.info("User connected to the EVE dashboard.")
    return render(request, 'eveonline/dashboard.html', context)

@login_required
@permission_required('audit_eve_character')
def view_characters(request):
    context = {}
    active_eve_users = User.objects.filter(guilds__slug="eve")
    context['mains'] = EveCharacter.objects.filter(main=None, user__in=active_eve_users)
    context['dreads'] = EveCharacter.objects.filter(character_alt_type="dread_alt", user__in=active_eve_users)
    context['carriers'] = EveCharacter.objects.filter(character_alt_type="carrier_alt", user__in=active_eve_users)
    context['supers'] = EveCharacter.objects.filter(character_alt_type="super_alt", user__in=active_eve_users)
    context['faxes'] = EveCharacter.objects.filter(character_alt_type="fax_alt", user__in=active_eve_users)
    return render(request, 'eveonline/view_characters.html', context)


@login_required
@permission_required('audit_eve_character')
def view_character(request, character):
    context = {}
    character = EveCharacter.objects.get(character_id=character)
    context['character'] = character
    token = character.token
    token.refresh()
    try:
        try:
            data = get_character_data(request, token)
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Failed to load, refresh. If this persists, pass it on to Bear. Exception: %s' % e)
        try:
            context['wallet'] = data['journal']
        except:
            context['wallet'] = None
            messages.add_message(request, messages.ERROR, 'Wallet failed to load.')
        try:
            context['net_worth'] = '{:20,}'.format(int(data['wallet']))
        except:
            context['net_worth'] = None
            messages.add_message(request, messages.ERROR, 'Net worth failed to load.')
        try:
            context['mails'] = data['mails']
        except:
            messages.add_message(request, messages.ERROR, 'Mails failed to load.')
            context['mails'] = None
        try:
            context['contacts'] = data['contacts']
        except:
            messages.add_message(request, messages.ERROR, 'Contacts failed to load.')
            context['contacts'] = None
        try:
            context['contracts'] = data['contracts']
        except:
            messages.add_message(request, messages.ERROR, 'Contracts failed to load.')
            context['contracts'] = None

        try:
            # context['skill_tree'] = data['skill_tree']
            context['sp'] = '{:20,}'.format(int(data['sp']))
        except:
            messages.add_message(request, messages.ERROR, 'Skills failed to load.')
            # context['skill_tree'] = None
            context['sp'] = None
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Could not load character. ' + str(e))
        return redirect('eve-dashboard')


    return render(request, 'eveonline/view_character.html', context)

@login_required
def set_main_character(request, character):
    eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
    eve_alts = EveCharacter.objects.filter(~Q(character_id=character), user=request.user)
    eve_character.main = None
    eve_character.character_alt_type = None
    eve_character.save()
    for alt in eve_alts:
        alt.main = eve_character
        alt.character_alt_type = None
        alt.save()
    return redirect('eve-dashboard')

@login_required
def set_alt_character(request, character, alt_type):
    eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
    eve_character_main = EveCharacter.objects.get(user=request.user, main=None)
    eve_character.main = eve_character_main
    eve_character.character_alt_type = alt_type
    eve_character.save()
    return redirect('eve-dashboard')

"""
Helper Functions
Used for the above web calls
"""
def get_character_data(request, token):
    eve_character = EveCharacter.objects.get(token=token)
    logger.info("Starting EVE Online Audit for Character: %s" % eve_character.character_name)
    start = time.time()
    token.refresh()
    eve_settings.ESI_SECURITY.update_token(token.populate())
    name_scopes = {
                   'skills': 'get_characters_character_id_skills',
                   'mails': 'get_characters_character_id_mail',
                   'journal': 'get_characters_character_id_wallet_journal',
                   'contacts': 'get_characters_character_id_contacts',
                   'contracts': 'get_characters_character_id_contracts',
                   'wallet': 'get_characters_character_id_wallet'
                   }
    data = {}
    data['character_id'] = eve_character.character_id
    for scope in name_scopes:
        op = eve_settings.ESI_APP.op[name_scopes[scope]](character_id=eve_character.character_id)
        response = eve_settings.ESI_CLIENT.request(op)
        if response.status == 200:
            data[scope] = response.data
        else:
            logger.info("Bad response for %s: %s" % (scope, response.status))
            try:
                logger.info("Response: %s" % response.json())
            except:
                pass

    data['sp'] = data['skills']['total_sp']
    if 'journal' in data:
        try:
            data = clean_character_journal(data)
        except Exception as e:
            logger.info("[AUDIT] Journal failed to load with %s" % e)
    if 'mails' in data:
        try:
            data = clean_mail_results(data)
        except Exception as e:
            logger.info("[AUDIT] Mails failed to load with %s" % e)
    if 'contracts' in data:
        try:
            data = clean_contracts(data)
        except Exception as e:
            logger.info("[AUDIT] Contracts failed to load with %s" % e)
    if 'contacts' in data:
        try:
            data = clean_contacts(data)
        except Exception as e:
            logger.info("[AUDIT] Contacts failed to load with %s" % e)
    logger.info("EVE Online audit for %s finished in %s seconds." % (eve_character.character_name, str(time.time() - start)))
    return data

def clean_character_journal(data):
    query = []
    journal = data['journal']
    if journal:
        for entry in journal:
            if 'first_party_id' in entry:
                query.append(entry.first_party_id)
            if 'second_party_id' in entry:
                query.append(entry.second_party_id)
        op = eve_settings.ESI_APP.op['post_universe_names'](ids=query)
        response = eve_settings.ESI_CLIENT.request(op)
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
        if int(mail['from']) < 145000000 or mail['from'] > 146000000:
            character_ids.add(mail['from'])
        for recipient in mail['recipients']:
            if recipient['recipient_type'] != "mailing_list":
                character_ids.add(recipient['recipient_id'])
    character_ids = list(character_ids)

    op = eve_settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = eve_settings.ESI_CLIENT.request(op).data
    for character in character_ids:
        for mail in data['mails']:
            if str(mail['from']) == str(character['id']):
                mail['from'] = character['name']
            for recipient in mail['recipients']:
                if str(recipient['recipient_id']) == str(character['id']):
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
    # Add mail data
    for mail in data['mails']:
        op = eve_settings.ESI_APP.op['get_characters_character_id_mail_mail_id'](character_id=data['character_id'], mail_id=mail['mail_id'])
        mail_body = eve_settings.ESI_CLIENT.request(op).data
        if 'body' in mail_body:
            mail['body'] = mail_body['body']
        else:
            mail['body'] = "UNABLE TO PULL BODY."
    return data

def clean_contacts(data):
    character_ids = []
    for contact in data['contacts']:
        character_ids.append(contact['contact_id'])
    op = eve_settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = eve_settings.ESI_CLIENT.request(op).data
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
    op = eve_settings.ESI_APP.op['post_universe_names'](ids=character_ids)
    character_ids = eve_settings.ESI_CLIENT.request(op).data
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

# def build_skill_tree(data):
#     with open('/home/auth/kryptedauth/app/games/eveonline/dumps/skills.txt') as skills:
#         skills_template = json.load(skills)
#         skills_tree = {}
#         player_skills = data['skills']['skills']
#
#         # Build the skill tree from Template
#         for category in skills_template:
#                 skills_tree[category] = {}
#                 print(skills_tree)
#                 for skill in skills_template[category][1]:
#                     skills_tree[category][skill] = [skills_template[category][1][skill], "0"]
#         for skill in player_skills:
#             for category in skills_tree:
#                 for skill_id in skills_tree[category]:
#                     if int(skill['skill_id']) == int(skill_id):
#                         skills_tree[category][skill_id][1] = skill['trained_skill_level']
#         data['skill_tree'] = skills_tree
#         data['sp'] = data['skills']['total_sp']
#     return data
