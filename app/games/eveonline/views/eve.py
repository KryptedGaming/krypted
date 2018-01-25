from django.shortcuts import render, redirect
from games.eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Guild
from core.decorators import login_required
from core.views.base import get_global_context
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.
@login_required
def dashboard(request):
    context = get_eve_context(request)
    return render(request, 'eveonline/dashboard.html', context)

@login_required
def apply(request):
    if EveCharacter.objects.filter(user=request.user).exists():
        return redirect('hr-create-application', slug='eve')
    else:
        messages.error(request, "You must add EVE characters before applying to this guild.")
        return redirect('eve-dashboard')

@login_required
def view_character(request, character):
    context = get_eve_context(request)
    character = EveCharacter.objects.get(token__character_id=character)
    context['character'] = character
    token = character.token
    try:
        token.refresh()
    except:
        return redirect('eve-dashboard')


    context['wallet'] = get_character_wallet(token)

    return render(request, 'eveonline/view_character.html', context)

def get_eve_context(request):
    context = get_global_context(request)
    user = request.user
    group = Group.objects.get_or_create(name='EVE')
    if group in user.groups.all():
        context['in_guild'] = True
    else:
        context['in_guild'] = False
    context['characters'] = EveCharacter.objects.filter(user=user)
    return context

def get_character_wallet(token):
    settings.ESI_SECURITY.update_token(token.populate())
    op = settings.ESI_APP.op['get_characters_character_id_wallet_journal'](character_id=token.character_id)

    try:
        wallet = settings.ESI_CLIENT.request(op)
    except:
        print("WALLET FAILED")
    else:
        query = []
        if wallet.data:
            for data in wallet.data:
                try:
                    query.append(data.first_party_id)
                    query.append(data.second_party_id)
                except:
                    pass

            try:
                op = settings.ESI_APP.op['post_universe_names'](ids=query)
                resolved = settings.ESI_CLIENT.request(op)
            except:
                pass
            else:
                counter1 = 0
                counter2 = 0
                for value in resolved.data:
                    counter1 += 1
                    for data in wallet.data:
                        counter2 += 2
                        try:
                            if data.first_party_id == value.id:
                                # print("Setting data player1 to id:: " + str(data.first_party_id) + " - " + value.name)
                                data.first_party_id = value.name
                                # print(data)
                            elif data.second_party_id == value.id:
                                # print("Setting data player2 to id")
                                data.second_party_id = value.name
                        except:
                            data['first_party_id'] = None
                            data['second_party_id'] = None
                print(counter1)
                print(counter2)
        else:
            print("Wallet returned a value of none. ESI issue?")
    return wallet.data

@login_required
def set_main_character(request, character):
    eve_character = EveCharacter.objects.get(token__character_id=character, user=request.user)
    eve_alts = EveCharacter.objects.filter(~Q(token__character_id=character), user=request.user)
    eve_character.main = None
    eve_character.character_alt_type = None
    eve_character.save()
    for alt in eve_alts:
        alt.main = eve_character_main
        alt.character_alt_type = None
        alt.save()
    return redirect('eve-dashboard')

def set_alt_character(request, character, alt_type):
    try:
        eve_character = EveCharacter.objects.get(character_id=character, user=request.user)
        eve_character_main = EveCharacter.objects.get(user=request.user, main=None)
        eve_character.main = eve_character_main
        eve_character.character_alt_type = alt_type
        eve_character.save()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=404)
