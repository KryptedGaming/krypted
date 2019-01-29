# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
# LOCAL IMPORTS
from modules.engagement.views.views import EventCreate, EventUpdate, EventDelete
# EXTERNAL IMPORTS
from modules.engagement.models import Event


@login_required
def dashboard(request):
    user_events = Event.objects.filter(group__in=request.user.groups.all())
    user_events = user_events.union(Event.objects.filter(group=None))

    context = {
        'user'   : request.user,
        'events' : user_events,
    }
    return render(request, 'events/events.html', context)

@login_required
def view_event(request,pk):
    context = {}
    context['event'] = Event.objects.get(pk=pk)
    return render(request, 'events/view_event.html', context)

@login_required
@permission_required('add_event')
def add_event(request):
    return EventCreate.as_view()(request)

@login_required
@permission_required('change_event')
def edit_event(request,*args,**kwargs):
    event = Event.objects.get(pk=kwargs['pk'])
    return EventUpdate.as_view()(request,*args,**kwargs)

@login_required
@permission_required('delete_event')
def remove_event(request,*args,**kwargs):
    event = Event.objects.get(pk=kwargs['pk'])
    return EventDelete.as_view()(request,*args,**kwargs)

@login_required
def add_event_registrant(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    event.registrants.add(request.user)
    messages.add_message(request, messages.SUCCESS, "Your registration for event '%s' has been recorded" % event.name)
    return redirect('all-events')

@login_required
def remove_event_registrant(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    event.registrants.remove(request.user)
    messages.add_message(request, messages.ERROR, "Your unregristration for event '%s' has been recorded" % event.name)
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
            messages.add_message(request, messages.SUCCESS, "Participation registered for '%s'" % event.name)
            return redirect('all-events')
    messages.add_message(request, messages.ERROR, "Incorrect password for '%s'" % event.name)
    return redirect('all-events')
