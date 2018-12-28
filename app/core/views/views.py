# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
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
# EXTERNAL IMPORTS
from app.conf import discourse as discourse_settings
# MISC
import logging, datetime, pytz, uuid, random

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

class BoxedField(Field):
    template='crispy_template/field.html'
    def __init__(self,*args,**kwargs):
        super(BoxedField,self).__init__(*args,**kwargs)

class EventCreate(CreateView):
    template_name='events/add_event.html'
    model = Event
    fields = ['guild','name','description','start_datetime'];
    success_url = reverse_lazy('all-events')

    def form_valid(self,form):
        # The user that creates the Event is the owner
        user = self.request.user
        form.instance.user = user
        form.instance.password = random.randint(100,999)
        return super(EventCreate,self).form_valid(form)

    def get_form(self, form_class=None):
        form = super(EventCreate, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_method = 'POST'
        onclick = "location.href='%s'" % reverse_lazy('all-events')
        form.helper.layout = Layout(
            *[BoxedField(f) for f in self.fields],
            FormActions(
                Submit('Create Event','Create Event', css_class='btn-success'),
                Button('Cancel','Cancel', css_class='btn-danger', onclick=onclick)
            )
        )
        form.fields['guild'].queryset = self.request.user.guilds.all()
        return form

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'description', 'start_datetime']
    template_name = "events/edit_event.html"
    success_url = reverse_lazy('all-events')
    def get_form(self, form_class=None):
        form = super(EventUpdate, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_method = 'POST'
        onclick = "location.href='%s'" % reverse_lazy('all-events')
        form.helper.layout = Layout(
            *[BoxedField(f) for f in self.fields],
            FormActions(
                Submit('Modify Event','Modify Event', css_class='btn-warning'),
                Button('Cancel','Cancel', css_class='btn-danger', onclick=onclick)
            )
        )
        return form

class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('all-events')
    template_name = "events/delete_event.html"
