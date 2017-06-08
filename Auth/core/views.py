from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event

## BASE
def dashboard(request):
    if request.user.is_authenticated():
        user = request.user

        # Get User Profile
        if Profile.objects.filter(user=user).count() > 0:
            profile = Profile.objects.get(user=user)
        else:
            profile = None

        # Get Notifications
        if Notification.objects.filter(user=user).count() > 0:
            notifications = Notification.objects.filter(user=user)
        else:
            notifications = None

    else:
        return redirect('login')

    return render(
            request,
            'dashboard/dashboard.html',
            context={
                'user': user,
                'notifications': notifications,
                'profile' : profile
                }
            )

## USER AUTHENTICATION
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                    password = request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(
            request,
            'accounts/login.html',
            context={
                'form': form,
                }
            )

def register_user(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password'],
                    )
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(
            request,
            'accounts/register.html',
            context={}
            )

def logout_user(request):
    return redirect('login')

## PROFILES 
def all_profiles(request):
    if request.user.is_authenticated():
        user = request.user
        profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        if user.groups.filter(name__in=['Officer', 'Leadership', 'Admin']).exists():
            return render(
                    request,
                    'models/profiles/all_profiles.html',
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
                'models/profiles/view_profile.html',
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
                'models/profiles/create_profile.html',
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
                'models/profiles/modify_profile.html',
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

## EVENTS
def all_events(request):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        valid_event_categories = []
        groups = user.groups.all()
        events = Event.objects.filter(game__in=groups)

        return render(
                request,
                'models/events/all_events.html',
                context={
                    'user': user,
                    'profile': user_profile,
                    'notifications': notifications,
                    'events': events
                    }
                )
    else:
        return redirect('login')



## NOTIFICATIONS
def all_notifications(request, username):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return render(request, 'models/notifications/all_notitifications.html', context={})
    else:
        return redirect('login')

def view_notification(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return render(request, 'models/notifications/view_notification.html', context={})
    else:
        return redirect('login')

def create_notification(request):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return render(request, 'models/notifications/create_notification.html', context={})
    else:
        return redirect('login')

def delete_notification(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return redirect('dashboard')
    else:
        return redirect('login')

def modify_notification(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)
        return render(request, 'models/notifications/modify_notification.html', context={})
    else:
        return redirect('login')

## GAMES
#def all_games(request):
#    if request.user.is_authenticated():
#        user = request.user
#        user_profile = Profile.objects.get(user=user)
#        notifications = Notification.objects.filter(user=user)
#        return render(request, 'models/games/all_games.html', context={})
#    else:
#        return redirect('login')
#
#def view_game(request, pk):
#    if request.user.is_authenticated():
#        user = request.user
#        user_profile = Profile.objects.get(user=user)
#        notifications = Notification.objects.filter(user=user)
#        return render(request, 'models/games/view_game.html', context={})
#    else:
#        return redirect('login')
#
#def create_game(request):
#    if request.user.is_authenticated():
#        user = request.user
#        user_profile = Profile.objects.get(user=user)
#        notifications = Notification.objects.filter(user=user)
#        return render(request, 'models/games/create_game.html', context={})
#    else:
#        return redirect('login')
#
#def delete_game(request, pk):
#    if request.user.is_authenticated():
#        user = request.user
#        user_profile = Profile.objects.get(user=user)
#        notifications = Notification.objects.filter(user=user)
#        return redirect('dashboard')
#    else:
#        return redirect('login')
#
#def modify_game(request, pk):
#    if request.user.is_authenticated():
#        user = request.user
#        user_profile = Profile.objects.get(user=user)
#        notifications = Notification.objects.filter(user=user)
#        return render(request, 'models/games/modify_game.html', context={})
#
#    else:
#        return redirect('login')
## MISC
def no_permissions(request):
    return render(request, 'misc/no_permissions.html', context={})
