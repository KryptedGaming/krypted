from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
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
    context={}
    code = request.GET['code']
    context['code'] = code
    context['encode'] = base64.b64encode(settings.DISCORD_CLIENT_ID + ":" + settings.DISCORD_SECRET)
    encode = base64.b64encode(settings.DISCORD_CLIENT_ID + ":" + settings.DISCORD_SECRET)
    res = requests.post('https://discordapp.com/api/oauth2/token?grant_type=authorization_code&code=' + code + '&redirect_uri=https%3A%2F%2Fdev.kryptedgaming.com%2Fdiscord%2Fcallback', headers={'Authorization': "Basic " + encode})
    context['token'] = request.GET
    context['request'] = res
    context['response'] = res.json()
    json = res.json()
    token = json['access_token']
    context['token'] = token
    me_data = requests.get('https://discordapp.com/api/users/@me', headers={'Authorization': "Bearer " + token})
    context['me'] = me_data.json()
    join_data = requests.post('https://discordapp.com/api/invites/MHtkWwm', headers={'Authorization': "Bearer " + token})
    context['join'] = join_data.json()
    return render(request, 'stupid.html', context)
