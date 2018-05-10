from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from requests_oauthlib import OAuth2Session
from modules.discord.models import DiscordUser
import logging
import base64
import requests

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    scope = (['email', 'guilds.join', 'identify'])
    redirect_uri = settings.DISCORD_CALLBACK_URL
    oauth = OAuth2Session(settings.DISCORD_CLIENT_ID, redirect_uri=redirect_uri, scope=scope, token=None, state=None)
    url,state = oauth.authorization_url(settings.DISCORD_BASE_URI)
    return HttpResponseRedirect(url)

def callback(request):
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_SECRET,
        "grant_type": "authorization_code",
        "code": request.GET['code'],
        "redirect_uri": settings.DISCORD_CALLBACK_URL
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('%s/oauth2/token' % settings.DISCORD_API_ENDPOINT, data, headers)
    r.raise_for_status()

    json = r.json()
    token = json['access_token']
    print(json)
    me = requests.get('https://discordapp.com/api/users/@me', headers={'Authorization': "Bearer " + token}).json()
    join = requests.post(settings.DISCORD_INVITE_LINK, headers={'Authorization': "Bearer " + token}).json()
    # Catch errors
    if not me['email']:
        messages.add_message(request, messages.ERROR, 'Could not find an email on your Discord profile. Please make sure your not signed in as a Guest Discord user.')
        return redirect('dashboard')
    # Delete old token if exists
    if DiscordUser.objects.filter(id=me['id']).count() > 0:
        token = DiscordUser.objects.get(id=me['id'])
        token.delete()
    # Create new token
    token = DiscordUser(
        access_token = json['access_token'],
        refresh_token = json['refresh_token'],
        id = me['id'],
        username = me['username'] + "#" + me['discriminator'],
        email = me['email'],
        user = request.user
    )
    token.save()

    return redirect('dashboard')
