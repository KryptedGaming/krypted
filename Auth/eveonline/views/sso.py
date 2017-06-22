from django.shortcuts import render,redirect
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
from eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User


# Create your views here.
def add_token(request):
    return redirect(settings.ESI_URL_CACHE)

def remove_token(request):
    pass

def refresh_token(request):
    pass

def receive_token(request):
    if request.user.is_authenticated():
        ## SSO PROCESS
        esi_app = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

        esi_security = EsiSecurity(
            app=esi_app,
            redirect_uri='http://localhost:8000/oauth/callback',
            client_id='d4f29f2a7dfa43978d8aaa3d1492a76f',
            secret_key='TvDAQTa6ApSEdGENPhdAOlhngrhHguDgSfARB6WH',
        )

        esi_client = EsiClient(esi_security)

        code = request.GET.get('code', None)
        esi_token = esi_security.auth(code)
        esi_verified = esi_security.verify()

        ## CHECK IF TOKEN OF SAME CHARACTER EXISTS
        if Token.objects.filter(character_name=esi_verified['CharacterName']).count() > 0:
            token = Token.objects.get(character_name=esi_verified['CharacterName'])
            token.delete()


        ## CREATE TOKEN
        token = Token(
                character_id=esi_verified['CharacterID'],
                character_owner_hash=esi_verified['CharacterOwnerHash'],
                character_name=esi_verified['CharacterName'],
                access_token=esi_token['access_token'],
                refresh_token=esi_token['refresh_token'],
                expires_in=esi_token['expires_in'],
                user=request.user
                )
        token.save()

        ## CREATE CHARACTER
        esiclient = EsiClient(
            security=esi_security,
            cache=None,
            headers={'User-Agent': 'User-Agent'}
        )

        op = esi_app.op['get_characters_character_id_portrait'](character_id=token.character_id)

        portrait = esiclient.request(op)

        character = EveCharacter(
                character_name=esi_verified['CharacterName'],
                character_portrait=portrait.data['px64x64'],
                token=token,
                user=request.user
        )
        character.save()

        return redirect('/eve')
    else:
        return redirect('login')
