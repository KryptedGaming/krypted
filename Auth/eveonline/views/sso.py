from django.shortcuts import render,redirect
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings
from eveonline.models import Token



# Create your views here.
def add_token(request):
    return redirect(settings.ESI_URL_CACHE)

def remove_token(request):
    pass

def refresh_token(request):
    pass

def receive_token(request):
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

    token = Token(
            character_id=esi_verified['CharacterID'],
            character_owner_hash=esi_verified['CharacterOwnerHash'],
            character_name=esi_verified['CharacterName'],
            access_token=esi_token['access_token'],
            refresh_token=esi_token['refresh_token']
            )
    token.save()

    return redirect('/eve')
