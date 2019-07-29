# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from app.forms import UserRegisterForm


def dashboard(request):
    return render(request, 'app/index.html', context={})


class UserRegister(FormView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('app-user-login')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            is_active=False
        )
        user.save()


class UserLogin(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('app-user-login')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            is_active=False
        )
        user.save()
