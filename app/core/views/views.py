# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# LOCAL IMPORTS
from core.forms import LoginForm, RegisterForm, ProfileForm
from core.decorators import login_required, services_required, permission_required
from core.models import *
# EXTERNAL IMPORTS
from app.conf import discourse as discourse_settings
# MISC
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    context['forum_url'] = discourse_settings.DISCOURSE_BASE_URL
    return render(request, 'base/dashboard.html', context)

class EventCreate(CreateView):
    template_name='events/add_event.html'
    model = Event
    fields = ['guild','name','description','start_datetime','user'];

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'description', 'start_datetime', 'user', 'guild']
    template_name = "events/edit_event.html"

class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('all-events')
    template_name = "events/delete_event.html"
