# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordResetConfirmView
from accounts.forms import UserRegisterForm, UserLoginForm
from accounts.models import UserInfo
from accounts.utilities import username_or_email_resolver


def activate_account(request, token):
    user = User.objects.filter(info__secret=token).first()
    if user:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Account activated. Please log in.')
        return redirect('accounts-login')
    else:
        messages.add_message(request, messages.ERROR,
                             'Unable to activate account. Contact support.')
        return redirect('accounts-login')


class UserRegister(FormView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts-login')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            is_active=False
        )
        user.save()

        user_info = UserInfo(
            user=user,
            age=form.cleaned_data['age'],
            country=form.cleaned_data['country']
        )
        user_info.save()
        return super().form_valid(form)


class UserLogin(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('accounts-login')

    def get_success_url(self):
        if 'next' in self.request.GET:
            return request.GET['next']
        return reverse_lazy('app-dashboard')

    def form_valid(self, form):
        # resolve username from email if needed
        username = username_or_email_resolver(form.cleaned_data['username'])
        # authenticate
        user = authenticate(username=username,
                            password=form.cleaned_data['password'])
        # login
        login(self.request, user)

        # resolve next url if redirect
        return super().form_valid(form)


class UserView(View):
    def get(self, request, username):
        context = {}
        context['user'] = User.objects.get(username=username)
        return render(request, context=context, template_name='accounts/user_view.html')

    def put(self, request, username):
        pass

    def delete(self, request, username):
        user = User.objects.get(username=username)
        if request.user == user:
            messages.add_message(request, messages.SUCCESS,
                                 'Account succesfully deleted, sorry to see you go!')
            user.delete()
        else:
            messages.add_message(request, messages.DANGER,
                                 'Nice try, but that is not your account.')

        return redirect('app-register')
