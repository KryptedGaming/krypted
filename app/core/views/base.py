from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event, Guild

## BASE
@login_required
def dashboard(request):
    context = get_global_context(request)
    return render(request, 'base/dashboard.html', context)

@login_required
def guilds(request):
    context = get_global_context(request)
    if not context['profile']:
        return redirect('create-profile')
    context['guilds'] = Guild.objects.all()
    return render(request, 'base/guilds.html', context)

@login_required
def games(request):
    context = get_global_context(request)
    if not context['profile']:
        return redirect('create-profile')
    context['games'] = Game.objects.all()
    return render(request, 'base/games.html', context)

@login_required
def notifications(request):
    context = get_global_context(request)
    context['all_notifications'] = Notification.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user, read=False)
    for notification in notifications:
        notification.read = True
        notification.save()

    return render(request, 'base/notifications.html', context)

@login_required
def profile(request):
    context = get_global_context(request)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            print("valid")
            context['profile'].biography = request.POST.get('biography')
            context['profile'].timezone = request.POST.get('timezone')
            context['profile'].user.first_name = request.POST.get('first_name')
            context['profile'].user.email = request.POST.get('email')
            context['profile'].save()
            context['profile'].user.save()
            return redirect('profile')
    else:
        form = ProfileForm()

    context['form'] = form
    return render(request, 'accounts/profile.html', context)

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

    # Get Admin
    if set(settings.ADMIN_ROLES) & set([group.name for group in user.groups.all()]):
        admin = True
    else:
        admin = False

    # Check services
    from modules.slack.models import SlackUser
    from modules.discord.models import DiscordToken
    from modules.discourse.models import DiscourseUser
    if SlackUser.objects.filter(user=user).count() > 0:
        slack_user = True
    else:
        slack_user = False
    if DiscordToken.objects.filter(user=user).count() > 0:
        discord_user = True
    else:
        discord_user = False
    if DiscourseUser.objects.filter(auth_user=user).count() > 0:
        discourse_user = True
    else:
        discourse_user = False


    context = {
        'user': user,
        'notifications': notifications,
        'profile': profile,
        'admin': admin,
        'slack_user': slack_user,
        'discourse_user': discourse_user,
        'discord_user': discord_user,
    }

    return context

def error_500(request):
    return render(request, 'global/500.html', context={})
