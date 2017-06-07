from django.shortcuts import render, redirect
from core.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

## BASE
def dashboard(request):
    if request.user.is_authenticated():
        user = request.user

    return render(
            request,
            'dashboard/dashboard.html',
            context={
                'user': user,
                }
            )

## USER AUTHENTICATION
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                    password = request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(
            request,
            'accounts/login.html',
            context={
                'form': form,
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
            context={}
            )

def logout_user(request):
    return redirect('login')
