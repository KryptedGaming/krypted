from django.contrib.auth.models import User
from django.shortcuts import redirect
from modules.discord.models import DiscordToken

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            if DiscordToken.objects.filter(user=request.user).count() == 0:
                return redirect('discord_index')
            return function(request, *args, **kw)
    return wrapper
