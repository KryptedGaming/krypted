from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event

## BASE
@login_required
def dashboard(request):
    user = request.user

    # Get User Profile
    if Profile.objects.filter(user=user).count() > 0:
        profile = Profile.objects.get(user=user)
    else:
        profile = None

    # Get Notifications
    if Notification.objects.filter(user=user).count() > 0:
        notifications = Notification.objects.filter(user=user)
    else:
        notifications = None

    return render(
            request,
            'dashboard/dashboard.html',
            context={
                'user': user,
                'notifications': notifications,
                'profile' : profile
                }
            )

## MISC
def no_permissions(request):
    return render(request, 'misc/no_permissions.html', context={})
