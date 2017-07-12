from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Profile, Notification, Game, Event
from . import base
from core.decorators import login_required

## NOTIFICATIONS
@login_required
def all_notifications(request, username):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user=user)
    return render(request, 'models/notifications/all_notitifications.html', context={})

def view_notification(request, pk):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user=user)
    return render(request, 'models/notifications/view_notification.html', context={})

def create_notification(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user=user)
    return render(request, 'models/notifications/create_notification.html', context={})

def delete_notification(request, pk):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user=user)
    return redirect('dashboard')

def modify_notification(request, pk):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user=user)
    return render(request, 'models/notifications/modify_notification.html', context={})


