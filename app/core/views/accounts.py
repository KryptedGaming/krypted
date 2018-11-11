from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from core.forms import LoginForm, RegisterForm, ProfileForm
from core.models import User, Group
from app.conf import discourse as discourse_settings
import uuid

"""
Views for User authentication
Includes everything related to registration and logging in
"""
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
                        return redirect(discourse_settings.DISCOURSE_BASE_URL)
                    return redirect(next)
                else:
                    return redirect('dashboard')
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                user = User.objects.get(username=request.POST['username'])
            username_invalid = not User.objects.filter(username=request.POST['username']).exists()
            email_invalid = not User.objects.filter(email=request.POST['username']).exists()
            if username_invalid and email_invalid:
                messages.add_message(request, messages.ERROR, 'That user does not exist. %s' % request.POST['username'])
            elif user and not user.is_active:
                if 'emails' not in request.session:
                    request.session['emails'] = 1
                else:
                    if request.session['emails'] > 3:
                        messages.add_message(request, messages.WARNING, 'You have requested too many emails. Please contact an admin on Discord.')
                        return redirect('login')
                    request.session['emails'] += 1
                user.activation_key = uuid.uuid4()
                user.save()
                messages.add_message(request, messages.WARNING, 'Please activate your account. And email has been sent.')
                send_mail(
                    'Verify your Krypted Account',
                    'Welcome to Krypted Gaming. \n Please click the following link to verify your account. \n' + settings.SERVER_DOMAIN + '/verify/confirmation/' + str(user.activation_key),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )
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
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    region=request.POST['region'],
                    activation_key=uuid.uuid4(),
                    is_active=False
                    )
            user.save()
            send_mail(
                'Verify your Krypted Account',
                'Welcome to Krypted Gaming. \n Please click the following link to verify your account. \n' + settings.SERVER_DOMAIN + '/verify/confirmation/' + str(user.activation_key),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            messages.add_message(request, messages.INFO, 'Please check your email to activate your account. It may be in your spam folder.')
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

def verify_confirm(request, token):
    if User.objects.filter(activation_key=token).exists():
        user=User.objects.get(activation_key=token)
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
