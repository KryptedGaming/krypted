# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.conf import settings


@login_required
def dashboard(request):
    if 'django_eveonline_connector' in settings.INSTALLED_APPS:
        from django_eveonline_connector.models import PrimaryEveCharacterAssociation
        if request.user.eve_tokens.all().count() > 1 and not PrimaryEveCharacterAssociation.objects.filter(user=request.user).exists():
            messages.warning(request, "You need to select a primary EVE Online character.")
            return redirect('django-eveonline-connector-character-select-primary')
    return redirect('accounts-user', username=request.user.username)
    
def handler500(request):
    return render(request, '500.html', status=505)
