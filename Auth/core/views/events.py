from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event
from . import base
## EVENTS
def all_events(request):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        group_tabs = []
        groups = user.groups.all()
        events = Event.objects.filter(group__in=groups)
        # Populate list of groups for pills
        for event in events:
            if event.group.name in group_tabs:
                pass
            else:
                group_tabs.append(event.group.name)

        return render(
                request,
                'models/events/all_events.html',
                context={
                    'user': user,
                    'profile': user_profile,
                    'notifications': notifications,
                    'events': events,
                    'groups': group_tabs
                    }
                )
    else:
        return redirect('login')

def view_event(request, pk):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        event = get_object_or_404(Event, pk=pk)
        if event.group in user.groups.all():
            return render(
                    request,
                    'models/events/view_event.html',
                    context={
                        'user': user,
                        'profile': user_profile,
                        'notifications': notifications,
                        'event': event
                        }
                    )
        else:
            return redirect('no_permissions')

