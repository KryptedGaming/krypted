# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
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
    return EventUpdate.as_view()(request,*args,**kwargs)

@login_required
def remove_event(request,*args,**kwargs):
    return EventDelete.as_view()(request,*args,**kwargs)

#
