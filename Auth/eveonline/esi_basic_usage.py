from django.shortcuts import render,redirect
from esipy import App, EsiClient, EsiSecurity
from django.conf import settings

esi_app = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

esi_security = EsiSecurity(
    app=esi_app,
    redirect_uri=settings.ESI_CALLBACK_URL,
    client_id=settings.ESI_CLIENT_ID,
    secret_key=settings.ESI_SECRET_KEY,
)

esi_security.get_auth_uri(scopes=settings.ESI_SCOPES)
