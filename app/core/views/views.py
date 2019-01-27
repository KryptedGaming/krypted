# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
# CRISPY FORMS IMPORTS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button
from crispy_forms.bootstrap import *
# LOCAL IMPORTS
from core.forms import LoginForm, RegisterForm
from core.decorators import login_required, services_required, permission_required
from core.models import *
from core.utils import username_or_email_resolver, send_activation_email
# MISC
import logging, datetime, pytz, uuid, random

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {}
    if apps.is_installed("modules.guild"):
        from modules.guild.models import Guild
        context['guilds'] = Guild.objects.all()

    if apps.is_installed('modules.discourse'):
        context['forum_url'] = apps.get_app_config('discourse').DISCOURSE_BASE_URL

    return render(request, 'core/dashboard.html', context)

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        # resolve next url if redirect
        if 'next' in self.request.GET:
            next = self.request.GET['next']
        else:
            next = None
        # resolve username from email if needed
        username = username_or_email_resolver(form.cleaned_data['username'])
        # authenticate user
        user = authenticate(username=username, password = form.cleaned_data['password'])
        # login
        login(self.request, user)
        # redirect handling
        if next:
            if apps.is_installed("modules.discourse"):
                if "discourse" in next:
                    return redirect(apps.get_app_config('discourse').DISCOURSE_BASE_URL)
            return redirect(next)
        else:
            return redirect('dashboard')

    def form_invalid(self, form):
        if 'attempts' not in self.request.session:
            self.request.session['attempts'] = 1
        else:
            self.request.session['attempts'] += 1

        if self.request.session['attempts'] >= 3:
            self.request.session['locked'] = str(datetime.datetime.utcnow())
        return super().form_invalid(form)

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'],
            is_active=False
        )
        user.save()
        user_info = UserInfo.objects.get(user=user)
        user_info.region = form.cleaned_data['region']
        user_info.age = form.cleaned_data['age']
        user_info.activation_key = uuid.uuid4()
        user_info.save()
        send_activation_email(User.objects.get(username=form.cleaned_data['username']))
        return redirect('login')

class UserUpdate(UpdateView):
    template_name='accounts/edit_user.html'
    success_url = reverse_lazy('dashboard')
    model = User
    fields = ['first_name', 'age', 'region']
