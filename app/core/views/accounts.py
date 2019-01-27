# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
# LOCAL IMPORTS
from core.decorators import login_required
from core.views.views import LoginView, RegisterView, UserUpdate
# MISC
import datetime

"""
Views for User authentication
Includes everything related to registration and logging in
"""
def login_user(request):
    # rate limit logins
    if 'locked' in request.session:
        time_delta = datetime.datetime.utcnow() - datetime.datetime.strptime(request.session['locked'], "%Y-%m-%d %H:%M:%S.%f")
        time_delta = time_delta.total_seconds()
        if time_delta < 300:
            return render(request, 'misc/locked.html', context={})
        else:
            request.session.pop('attempts', None)
            request.session.pop('locked', None)
    # redirect to form view
    return LoginView.as_view()(request)

def register_user(request):
    return RegisterView.as_view()(request)

@login_required
def edit_user(request, *args, **kwargs):
    if kwargs.get('pk') != str(request.user.pk):
        messages.error(request, "Nice try, guy")
        return redirect('dashboard')
    return UserUpdate.as_view()(request, *args, **kwargs)

def logout_user(request):
    logout(request)
    return redirect('login')

def verify_confirm(request, token):
    if User.objects.filter(info__activation_key=token).exists():
        user=User.objects.get(info__activation_key=token)
        user.is_active=True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account verified. Please log in.')
        return redirect('login')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to verify your account. Try again.')
        return redirect('login')
## HELPERS
def username_or_email_resolver(username):
    if User.objects.filter(email=username).exists():
        return User.objects.get(email=username).username
    else:
        return username
