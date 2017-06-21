from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event
from . import base
## PROFILES 
def all_profiles(request):
    if request.user.is_authenticated():
        user = request.user
        profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        if user.groups.filter(name__in=['Officer', 'Leadership', 'Admin']).exists():
            return render(
                    request,
                    'profiles/all_profiles.html',
                    context={
                        'profiles': Profile.objects.all(),
                        'profile': profile,
                        'notifications': notifications,
                        }
                    )
        else:
            return redirect('no_permissions')
    else:
        return redirect('login')

def view_profile(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return render(
                request,
                'profiles/view_profile.html',
                context={
                    'user_profile': user_profile,
                    'notifications': notifications,
                    'profile': Profile.objects.get(pk=pk),
                    }
                )
    else:
        return redirect('login')

def create_profile(request):
    if request.user.is_authenticated():
        user = request.user

        if request.method == 'POST':
            biography = request.POST.get('biography')
            game = request.POST.get('games')
            twitter = request.POST.get('twitter')
            steam = request.POST.get('steam')
            blizzard = request.POST.get('blizzard')

            profile = Profile(user=user)
            profile.save()
            if biography:
                profile.biography = biography
            if game:
                profile.games.add(game)
            if twitter:
                profile.twitter = twitter
            if steam:
                profile.steam = steam
            if blizzard:
                profile.blizzard = blizzard

            profile.save()

            return redirect('dashboard')
        else:
            form = ProfileForm()
        return render(
                request,
                'profiles/create_profile.html',
                context={
                    'form': form,
                    }
                )
    else:
        return redirect('login')

def delete_profile(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        if user_profile == Profile.objects.get(pk=pk):
            user_profile.delete()
            return redirect('dashboard')
        else:
            return redirect('no_permissions')
    else:
        return redirect('login')

def modify_profile(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        # Build list of currently added
        game_list = []
        for game in user_profile.games.all():
            game_list.append(game.title)
        games = Game.objects.exclude(title__in=game_list)

        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                user_profile.biography = request.POST.get('biography')
                user_profile.twitter = request.POST.get('twitter')
                user_profile.steam = request.POST.get('steam')
                user_profile.blizzard = request.POST.get('blizzard')
                user_profile.save()
                return redirect('view-profile', pk=user_profile.id)
        else:
            form = ProfileForm()

        return render(
                request,
                'profiles/modify_profile.html',
                context={
                    'form': form,
                    'biography': user_profile.biography,
                    'twitter': user_profile.twitter,
                    'steam': user_profile.steam,
                    'blizzard': user_profile.blizzard,
                    'games': Game.objects.all(),
                    'profile': user_profile,
                    'user': user
                    }
                )
    else:
        return redirect('login')

def profile_add_game(request, pk, game):
    if request.user.is_authenticated():
        user = request.user
        passed_profile = Profile.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=user)
        if passed_profile.id != user_profile.id:
            print(passed_profile.id)
            print(user_profile.id)
            return redirect('no_permissions')

        profile = Profile.objects.get(pk=pk)
        profile.games.add(Game.objects.get(id=game))
        profile.save()
        return redirect('modify-profile', pk=pk)

def profile_remove_game(request, pk, game):
     if request.user.is_authenticated():
        user = request.user
        passed_profile = Profile.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=user)
        if passed_profile.id != user_profile.id:
            print(passed_profile.id)
            print(user_profile.id)
            return redirect('no_permissions')

        profile = Profile.objects.get(pk=pk)
        profile.games.remove(Game.objects.get(id=game))
        profile.save()
        return redirect('modify-profile', pk=pk)


