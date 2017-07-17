from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import EventForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event
from . import base
from datetime import datetime
from core.views.base import get_global_context

## EVENTS
@login_required
def all_events(request):
    user = request.user
    context = get_global_context(request)

    # Populate groups and events
    group_tabs = []
    groups = user.groups.all()
    events = Event.objects.filter(group__in=groups).exclude(date_occuring__lte=datetime.now()).order_by('date_occuring')

    # Populate list of groups for pills
    for event in events:
        if event.group.name in group_tabs:
            pass
        else:
            group_tabs.append(event.group.name)

    context['events'] = events
    context['groups'] = group_tabs
    return render(
            request,
            'events/all_events.html',
            context)

@login_required
def view_event(request, pk):
    context = get_global_context(request)
    event = get_object_or_404(Event, pk=pk)
    context['event'] = event
    if event.group in request.user.groups.all():
        return render(
                request,
                'events/view_event.html',
                context
                )
    else:
        return redirect('no_permissions')

@login_required
def create_event(request):
    user = request.user

    if request.method == 'POST':
        date_occuring = request.POST.get('date_occuring')
        title = request.POST.get('title')
        description = request.POST.get('description')
        notes = request.POST.get('notes')
        game = request.POST.get('game')
        importance = request.POST.get('importance')
        group = Game.objects.get(pk=game).group
        event = Event(creator=request.user, date_occuring=date_occuring,
                title=title, description=description, importance=importance,
                notes=notes, group=group)
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

@login_required
def modify_event(request, pk):
    user = request.user
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event.date_occuring = request.POST.get('date_occuring')
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.notes = request.POST.get('notes')
        event.importance = request.POST.get('importance')
        event.save()
        return redirect('all-events')
    else:
        form = EventForm()
    return render(
            request,
            'events/modify_event.html',
            context={
                'form': form,
                'event': event,
                }
            )

@login_required
def delete_event(request, pk):
    user = request.user

    if user.has_perm('core.delete_event'):
        event = Event.objects.get(pk=pk)
        event.delete()
        return redirect('all-events')
    else:
        return redirect('no_permissions')

