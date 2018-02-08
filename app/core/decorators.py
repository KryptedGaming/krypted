from django.contrib.auth.models import User
from django.shortcuts import redirect
from modules.discord.models import DiscordToken
from core.models import Profile

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            if DiscordToken.objects.filter(user=request.user).count() == 0:
                return redirect('discord_index')
            return function(request, *args, **kw)
    return wrapper

def no_user_profile(function):
    def wrapper(request, *args, **kw):
        try:
            profile = Profile.objects.get(user=request.user)
            return redirect('profile')
        except:
            return function(request, *args, **kw)
    return wrapper
