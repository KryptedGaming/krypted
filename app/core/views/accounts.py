# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
# LOCAL IMPORTS
from core.decorators import services_required
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
    request.session['new_user'] = True 
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

@login_required
def new_user(request):
    request.session['eve_sso_redirect_override'] = "tutorial"
    return render(request, 'accounts/new_user.html', context={})

@login_required
@services_required
def new_user_complete(request): 
    if 'new_user' in request.session:
        request.session.pop('new_user')
    if 'eve_sso_redirect_override' in request.session:
        request.session.pop('eve_sso_redirect_override')
    return redirect('dashboard')

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
