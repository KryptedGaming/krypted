from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event, Guild
from . import base
from core.decorators import login_required
from core.views.base import get_global_context

@login_required
def create_profile(request):
    user = request.user

    if request.method == 'POST':
        biography = request.POST.get('biography')
        timezone = request.POST.get('timezone')

        profile = Profile(user=user, biography=biography, timezone=timezone)
        profile.save()

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
def delete_profile(request, pk):
    user_profile = Profile.objects.get(user=request.user)

    if user_profile == Profile.objects.get(pk=pk):
        user_profile.delete()
        return redirect('dashboard')
    else:
        return redirect('no_permissions')

@login_required
def profile_add_game(request, game_to_add):
    profile = Profile.objects.get(user=request.user)
    profile.games.add(Game.objects.get(id=game_to_add))
    profile.save()
    return redirect('games')

@login_required
def profile_remove_game(request, game):
    profile = Profile.objects.get(user=request.user)
    profile.games.remove(Game.objects.get(id=game))
    profile.save()
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
