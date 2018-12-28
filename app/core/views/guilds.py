# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
# LOCAL IMPORTS
from core.forms import LoginForm, RegisterForm
from core.decorators import login_required, services_required, permission_required
from core.models import *
# MISC
import logging

logger = logging.getLogger(__name__)

@login_required
@services_required
def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'base/guilds.html', context)
