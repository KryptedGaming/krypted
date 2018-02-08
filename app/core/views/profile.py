from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event, Guild
from . import base
from core.decorators import login_required
from core.views.base import get_global_context
from core.decorators import *

@login_required
@no_user_profile
def create_profile(request):
    user = request.user

    if request.method == 'POST':
        biography = request.POST.get('biography')
        timezone = request.POST.get('timezone')

        profile = Profile(user=user, biography=biography, timezone=timezone)
        profile.save()
        request.user.first_name = request.POST.get('first_name')
        request.user.save()
        Notification(message="You have created a profile.").notify_user(user)

        return redirect('dashboard')
    else:
        form = ProfileForm()
    return render(
            request,
            'accounts/create_profile.html',
            context={
                'form': form,
                }
            )

@login_required
def profile_add_game(request, game_to_add):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        if profile:
            profile.games.add(Game.objects.get(id=game_to_add))
            profile.save()
            Notification(message="You added game " +
             game_to_add + " to your account.").notify_user(user)
        else:
            return redirect('create-profile')
    except:
        Notification(message="You failed to add game " +
         game_to_add + " to your account.").notify_user(user)
    return redirect('games')

@login_required
def profile_remove_game(request, game):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        if profile:
            profile.games.remove(Game.objects.get(id=game))
            profile.save()
            Notification(message="You removed game " +
             game + " to your account.").notify_user(user)
        else:
            return redirect('create-profile')
    except:
        Notification(message="You failed to removed game " +
         game + " to your account.").notify_user(user)
    return redirect('games')

@login_required
def profile_add_guild(request, guild):
    profile = Profile.objects.get(user=request.user)
    profile.guilds.add(Guild.objects.get(id=guild))
    profile.save()
    return redirect('modify-profile', pk=profile.pk)
@login_required
def profile_remove_guild(request, guild):
    profile = Profile.objects.get(user=request.user)
    profile.guilds.remove(Guild.objects.get(id=guild))
    profile.save()
    return redirect('modify-profile', pk=profile.pk)
