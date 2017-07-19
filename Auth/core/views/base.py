from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event, Guild

## BASE
@login_required
def dashboard(request):
    context = get_global_context(request)
    return render(request, 'base/dashboard.html', context)

def guilds(request):
    context = get_global_context(request)
    print(context['profile'])
    context['guilds'] = Guild.objects.all()
    return render(request, 'base/guilds.html', context)

def games(request):
    context = get_global_context(request)
    print(context['profile'].games)
    context['games'] = Game.objects.all()
    return render(request, 'base/games.html', context)

## MISC
def no_permissions(request):
    return render(request, 'misc/no_permissions.html', context={})

def get_global_context(request):
    user = request.user

    # Get Profile
    if Profile.objects.filter(user=user).count() > 0:
        profile = Profile.objects.get(user=user)
    else:
        profile = None

    # Get Notifications
    if Notification.objects.filter(user=user).count() > 0:
        notifications = Notification.objects.filter(user=user, read=False)
    else:
        notifications = None

    context = {
        'user': user,
        'notifications': notifications,
        'profile': profile,
    }

    return context
