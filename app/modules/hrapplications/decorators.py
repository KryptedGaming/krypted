from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from modules.discord.models import DiscordUser
from modules.discourse.models import DiscourseUser
from games.eveonline.models import EveCharacter
import logging

logger = logging.getLogger(__name__)

def services_required(function):
    def wrapper(request, *args, **kw):
        discord_user_exists = DiscordUser.objects.filter(user=request.user).exists()
        discourse_user_exists = DiscourseUser.objects.filter(auth_user=request.user).exists()
        if discord_user_exists and discourse_user_exists:
            return function(request, *args, **kw)
        else:
            messages.add_message(request, messages.ERROR, 'Please complete your services on this page before creating your application.')
            return redirect('dashboard')
    return wrapper

def eve_characters_required(function):
    def wrapper(request, *args, **kw):
        eve_characters = EveCharacter.objects.filter(user=request.user)
        if eve_characters:
            return function(request, *args, **kw)
        else:
            messages.add_message(request, messages.ERROR, 'Please add EVE Characters before applying to the EVE Online guild.')
            messages.add_message(request, messages.WARNING, 'NOTE: Add ALL characters, even if you do not use them. Failure to do this will result in a rejected application.')
            return redirect('eve-dashboard')
    return wrapper
