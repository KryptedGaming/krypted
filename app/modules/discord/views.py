from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.apps import apps
from requests_oauthlib import OAuth2Session
from modules.discord.models import DiscordUser
import logging
import base64
import requests

discord_settings = apps.get_app_config('discord')
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    scope = (['email', 'guilds.join', 'identify'])
    redirect_uri = discord_settings.DISCORD_CALLBACK_URL
    oauth = OAuth2Session(discord_settings.DISCORD_CLIENT_ID, redirect_uri=redirect_uri, scope=scope, token=None, state=None)
    url,state = oauth.authorization_url(discord_settings.DISCORD_BASE_URI)
    return HttpResponseRedirect(url)

def callback(request):
    data = {
        "client_id": discord_settings.DISCORD_CLIENT_ID,
        "client_secret": discord_settings.DISCORD_SECRET,
        "grant_type": "authorization_code",
        "code": request.GET['code'],
        "redirect_uri": discord_settings.DISCORD_CALLBACK_URL
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('%s/oauth2/token' % discord_settings.DISCORD_API_ENDPOINT, data, headers)
    r.raise_for_status()

    json = r.json()
    token = json['access_token']
    me = requests.get('https://discordapp.com/api/users/@me', headers={'Authorization': "Bearer " + token}).json()
    join = requests.post(discord_settings.DISCORD_INVITE_LINK, headers={'Authorization': "Bearer " + token}).json()
    # Catch errors
    if not me['email']:
        messages.add_message(request, messages.ERROR, 'Could not find an email on your Discord profile. Please make sure your not signed in as a Guest Discord user.')
        return redirect('dashboard')
    # Delete old token if exists
    if DiscordUser.objects.filter(external_id=me['id']).count() > 0:
        token = DiscordUser.objects.get(external_id=me['id'])
        token.delete()
    # Create new token
    token = DiscordUser(
        access_token = json['access_token'],
        refresh_token = json['refresh_token'],
        external_id = me['id'],
        username = me['username'] + "#" + me['discriminator'],
        email = me['email'],
        user = request.user
    )
    token.save()

    return redirect('dashboard')
