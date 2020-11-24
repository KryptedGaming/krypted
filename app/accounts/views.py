# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView, DeleteView
from django.contrib.auth.views import PasswordResetConfirmView, LogoutView
from accounts.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
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
    template_name = 'accounts/authentication/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts-login')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'])
        # Check if email activation is enabled
        if not settings.EMAIL_HOST:
            user.is_active = True
        else:
            user.is_active = False
        user.save()

        user_info = UserInfo(
            user=user,
            age=form.cleaned_data['age'],
            country=form.cleaned_data['country'])
        user_info.save()
        return super().form_valid(form)


class UserLogin(FormView):
    template_name = 'accounts/authentication/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('accounts-login')

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']

        return "/"

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


class UserLogout(LogoutView):
    next_page = reverse_lazy('accounts-login')


@method_decorator(login_required, name='dispatch')
class UserView(View):
    def get(self, request, username):
        context = {}
        try:
            context['user'] = User.objects.select_related('info').get(
                username=username)
        except User.DoesNotExist:
            messages.add_message(
                self.request, messages.ERROR, "User does not exist.")
            return redirect("/")
        return render(request, context=context, template_name='accounts/profiles/my_profile.html')

    def post(self, request, username):
        request_data = request.POST.copy()
        user = User.objects.get(username=username)
        if not request.user == user:
            messages.add_message(self.request, messages.WARNING,
                                 "Nice try, but that is not your account.")
            return redirect('accounts-user', user.username)

        if 'username' in request_data and request_data['username'] == request.user.username:
            request_data.pop('username')

        if 'email' in request_data and request_data['email'] == request.user.email:
            request_data.pop('email')

        form = UserUpdateForm(request_data)
        if form.is_valid():
            if form.cleaned_data['username']:
                user.username = form.cleaned_data['username']
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
            user.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 "Account successfully updated.")
            return redirect('accounts-user', user.username)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 "Failed to update account information.")

        # Fill context
        context = {}
        context['form'] = form

        return render(request, context=context, template_name='accounts/profiles/my_profile.html')


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('accounts-login')
    template_name = 'accounts/authentication/user_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return redirect(success_url)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 'Nice try, but that is not your account.')
            return redirect("/")
