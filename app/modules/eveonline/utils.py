from esipy import App, EsiClient, EsiSecurity
from django.conf import settings

def generate_esi_session():
    esi_session = {}
    esi_session['app'] = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

    esi_session['security'] = EsiSecurity(
        app=esi_session['app'],
        redirect_uri=settings.ESI_CALLBACK_URL,
        client_id=settings.ESI_CLIENT_ID,
        secret_key=settings.ESI_SECRET_KEY,
        headers={'User-Agent': 'Krypted Authentication 2.0'}
    )

    esi_session['client'] = EsiClient(
        security=esi_session['security'],
        cache=None,
        headers={'User-Agent': 'Krypted Authentication 2.0'}
    )
    return esi_session
