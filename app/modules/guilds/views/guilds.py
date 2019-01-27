# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
# INTERNAL IMPORTS
from modules.guilds.models import Guild
# MISC
import logging
logger = logging.getLogger(__name__)


def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'guilds/guilds.html', context)
