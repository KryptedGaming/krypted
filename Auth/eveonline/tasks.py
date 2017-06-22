from celery import task
from eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User
from esipy import App, EsiClient, EsiSecurity

@task()
def verify_sso_tokens():
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
