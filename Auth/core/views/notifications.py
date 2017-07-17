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
def all_notifications(request, username):
    context = get_global_context(request)
    return render(request, 'notifications/all_notitifications.html', context)

@login_required
def view_notification(request, pk):
    context = get_global_context(request)
    return render(request, 'notifications/view_notification.html', context)

@login_required
def create_notification(request):
    context = get_global_context(request)
    return render(request, 'notifications/create_notification.html', context)

@login_required
def delete_notification(request, pk):
    context = get_global_context(request)
    return redirect('dashboard')

@login_required
def modify_notification(request, pk):
    context = get_global_context(request)
    return render(request, 'notifications/modify_notification.html', context)

@login_required
def read_notifications(request, path):
    notifications = Notification.objects.filter(user=request.user, read=False)
    for notification in notifications:
        notification.read = True
        notification.save()
    return redirect('dashboard')
