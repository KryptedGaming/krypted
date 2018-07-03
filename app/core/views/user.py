from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from core.models import Profile, Notification, Game, Event
from . import base
## USER AUTHENTICATION
def login_user(request):
    try:
        next = request.GET['next']
    except:
        next = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            resolved_username = username_or_email_resolver(request.POST['username'])
            user = authenticate(username=resolved_username,
                    password = request.POST['password'])
            if user is not None:
                login(request, user)
                if next:
                    if "discourse" in next:
                        return redirect(settings.DISCOURSE_BASE_URL)
                    return redirect(next)
                else:
                    return redirect('dashboard')
        else:
            username_invalid = not User.objects.filter(username=request.POST['username']).exists()
            email_invalid = not User.objects.filter(email=request.POST['username']).exists()
            if username_invalid and email_invalid:
                messages.add_message(request, messages.ERROR, 'That user does not exist. %s' % request.POST['username'])
            else:
                messages.add_message(request, messages.ERROR, 'Wrong username or password.')
            return redirect('login')
    else:
        form = LoginForm()
        return render(
                request,
                'accounts/login.html',
                context={
                    'form': form,
                    'next': next
                    }
                )

def register_user(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password'],
                    )
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(
            request,
            'accounts/register.html',
            context={
                'form': form
                }
            )


def logout_user(request):
    logout(request)
    return redirect('login')

## HELPERS
def username_or_email_resolver(username):
    if User.objects.filter(email=username).exists():
        return User.objects.get(email=username).username
    else:
        return username
