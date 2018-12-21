# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
# LOCAL IMPORTS
from core.forms import LoginForm, RegisterForm
from core.decorators import login_required, services_required, permission_required
from core.models import *
from core.utils import username_or_email_resolver, send_activation_email
# EXTERNAL IMPORTS
from app.conf import discourse as discourse_settings
# MISC
import logging, datetime, pytz, uuid

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    context['forum_url'] = discourse_settings.DISCOURSE_BASE_URL
    return render(request, 'base/dashboard.html', context)

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
            if "discourse" in next:
                return redirect(discourse_settings.DISCOURSE_BASE_URL)
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
            region = form.cleaned_data['region'],
            age = form.cleaned_data['age'],
            activation_key=uuid.uuid4(),
            is_active=False
        )
        user.save()
        send_activation_email(User.objects.get(username=form.cleaned_data['username']))
        return redirect('login')

class UserUpdate(UpdateView):
    template_name='accounts/edit_user.html'
    success_url = reverse_lazy('dashboard')
    model = User
    fields = ['first_name', 'age', 'region']

class EventCreate(CreateView):
    template_name='events/add_event.html'
    model = Event
    fields = ['guild','name','description','start_datetime','user'];

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'description', 'start_datetime', 'user', 'guild']
    template_name = "events/edit_event.html"

class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('all-events')
    template_name = "events/delete_event.html"
