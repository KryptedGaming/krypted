from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event, Guild
from core.views.base import get_global_context

## BASE
@login_required
def dashboard(request):
    context = get_global_context(request)
    return render(request, 'base/dashboard.html', context)
