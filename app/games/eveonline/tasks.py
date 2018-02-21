from __future__ import absolute_import, unicode_literals
from celery import task
from games.eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings

@task()
def verify_sso_tokens():
    print("weeeee")
    tokens = Token.objects.all()
    esi_app = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

    esi_security = EsiSecurity(
        app=esi_app,
        redirect_uri='http://localhost:8000/oauth/callback',
        client_id='d4f29f2a7dfa43978d8aaa3d1492a76f',
        secret_key='TvDAQTa6ApSEdGENPhdAOlhngrhHguDgSfARB6WH',
    )

    esiclient = EsiClient(
        security=esi_security,
        cache=None,
        headers={'User-Agent': 'User-Agent'}
    )

    for token in tokens:
        valid = True
        esi_security.update_token(token.populate())
        try:
            esi_security.refresh()
        except:
            valid = False

        if not valid:
            token.delete()

@task()
def sync_user_group(user):
    tokens = Token.objects.filter(user=user)
    for token in tokens:
        token.refresh()
    characters = EveCharacter.objects.filter(user=user)
    group_clear = True

    for character in characters:
        print(character)
        if character.character_corporation == settings.MAIN_CORPORATION_ID:
            print("Match")
            group_clear = False

    if not group_clear:
        if Group.objects.get(name="EVE") not in user.groups.all():
            user.groups.add(Group.objects.get(name="EVE"))
        else:
            pass
    else:
        user.groups.remove(Group.objects.get(name="EVE"))
