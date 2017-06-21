from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import EventForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event
from . import base
from datetime import datetime
## EVENTS
def all_events(request):
    if request.user.is_authenticated():
        user = request.user
        user_profile = Profile.objects.get(user=user)
        notifications = Notification.objects.filter(user=user)

        group_tabs = []
        groups = user.groups.all()
        events = Event.objects.filter(group__in=groups).exclude(date_occuring__lte=datetime.now()).order_by('date_occuring')
        # Populate list of groups for pills
        for event in events:
            if event.group.name in group_tabs:
                pass
            else:
                group_tabs.append(event.group.name)

        return render(
                request,
                'events/all_events.html',
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
                    'events/view_event.html',
                    context={
                        'user': user,
                        'profile': user_profile,
                        'notifications': notifications,
                        'event': event
                        }
                    )
        else:
            return redirect('no_permissions')

def create_event(request):
    if request.user.is_authenticated():
        user = request.user

        if request.method == 'POST':
            date_occuring = request.POST.get('date_occuring')
            title = request.POST.get('title')
            description = request.POST.get('description')
            notes = request.POST.get('notes')
            game = request.POST.get('game') 
            group = Game.objects.get(pk=game).group
            event = Event(creator=request.user, date_occuring=date_occuring,
                    title=title, description=description, notes=notes, group=group)
            event.save()

            return redirect('all-events')
        else:
            form = EventForm()
        return render(
                request,
                'events/create_event.html',
                context={
                    'form': form,
                    }
                )
    else:
        return redirect('login')

def modify_event(request, pk):
    pass
def delete_event(request, pk):
    pass
