from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from modules.discord.models import DiscordToken
from modules.discourse.models import DiscourseUser
from core.models import Profile

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return function(request, *args, **kw)
    return wrapper

def tutorial_complete(function):
    def wrapper(request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).count() == 0:
            messages.add_message(request, messages.ERROR, 'Please create a profile before accessing this area.')
            return redirect('create-profile')
        if DiscordToken.objects.filter(user=request.user).count() == 0:
            messages.add_message(request, messages.ERROR, 'Please link your Discord account before accessing this area. Click "Discord" under Services.')
            return redirect('dashboard')
        if DiscourseUser.objects.filter(auth_user=request.user).count() == 0:
            messages.add_message(request, messages.ERROR, 'Please create a Forum accuont before accessing this area. Click "Discourse" under Services.')
            return redirect('dashboard')
        return function(request, *args, **kwargs)
    return wrapper

def no_user_profile(function):
    def wrapper(request, *args, **kw):
        try:
            profile = Profile.objects.get(user=request.user)
            return redirect('profile')
        except:
            return function(request, *args, **kw)
    return wrapper
