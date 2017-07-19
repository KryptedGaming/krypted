from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event
from core.decorators import login_required
from core.views.base import get_global_context

## NOTIFICATIONS
@login_required
def notifications(request):
    context = get_global_context(request)
    context['all_notifications'] = Notification.objects.filter(user=request.user)

    notifications = Notification.objects.filter(user=request.user, read=False)
    for notification in notifications:
        notification.read = True
        notification.save()

    return render(request, 'notifications/all_notifications.html', context)
