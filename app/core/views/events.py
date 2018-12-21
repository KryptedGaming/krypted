# DJANGO IMPORTS
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# LOCAL IMPORTS
from core.models import Event, Guild
from core.decorators import login_required
from core.views.views import EventCreate, EventUpdate, EventDelete
# MISC
from datetime import datetime

@login_required
def dashboard(request):
    user_guilds = request.user.guilds.all()
    user_events = Event.objects.filter(guild__in=user_guilds);
    context = {
        'user'   : request.user,
        'events' : user_events.union(Event.objects.filter(guild=None)),
        'guilds' : user_guilds
    }
    return render(request, 'base/events.html', context)

@login_required
def view_event(request,pk):
    pass

@login_required
def add_event(request):
    return EventCreate.as_view()(request)

@login_required
def edit_event(request,*args,**kwargs):
    # TODO: Only the owner or staff can edit an event
    return EventUpdate.as_view()(request,*args,**kwargs)

@login_required
def remove_event(request,*args,**kwargs):
    # TODO: Only the owner or staff can remove an event
    return EventDelete.as_view()(request,*args,**kwargs)

@login_required
def add_event_registrant(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    event.registrants.add(request.user)
    messages.add_message(request, messages.SUCCESS, "You have registered for Event: %s" % event.name)
    return redirect('all-events')

@login_required
def remove_event_registrant(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    event.registrants.remove(request.user)
    messages.add_message(request, messages.ERROR, "You have unregistered for Event: %s" % event.name)
    return redirect('all-events')

@login_required
def add_event_participant(request, event_pk):
    """
    Adds a user to event participants if given the correct password
    Expects a GET parameter: password
    Example: <input type="text" name="password"> where form action is GET
    """
    event = Event.objects.get(pk=event_pk)
    if 'password' in request.GET:
        event_password = request.GET['password']
        if event_password == event.password:
            event.participants.add(request.user)
            messages.add_message(request, messages.SUCCESS, "Participation added for Event: %s" % event.name)
            return redirect('all-events')
    messages.add_message(request, messages.ERROR, "Incorrect Participation password for Event: %s" % event.name)
    return redirect('all-events')
