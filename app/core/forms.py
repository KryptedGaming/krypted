# DJANGO
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.conf import settings
# INTERNAL
from core.models import User
from core.utils import send_activation_email
# MISC
import logging

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, required=True)
    password = forms.CharField(max_length=32, required=True)

    def clean(self):
        input = self.cleaned_data
        username = self.resolve_username(input.get('username'))
        password = input.get('password')

        # checks
        user_exists = User.objects.filter(username=username).exists()
        user_authenticated = authenticate(username=username, password=password)
        if user_exists:
            user_active = User.objects.get(username=username).is_active

        # authenticate check
        if not user_authenticated:
            self.add_error('username', 'Invalid credentials.')
        if not user_exists:
            self.add_error('username', 'User does not exist.')
        if user_exists and not user_active:
            self.activate_user(username)
            self.add_error('username', 'Account not active, please check your email')

        return input

    def resolve_username(self, username):
        email_valid = User.objects.filter(email=username).exists()
        if email_valid:
            return User.objects.get(email=username).username
        else:
            return username

    def activate_user(self, username):
        user = User.objects.get(username=username)
        send_activation_email(user)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    email = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=32, required=True)
    vpassword = forms.CharField(max_length=32, required=True)
    region = forms.ChoiceField(choices=settings.REGIONS, required=True)
    age = forms.IntegerField()

    def clean(self):
        input = self.cleaned_data
        password = input.get('password')

        if User.objects.filter(username=input.get('username')).exists():
            self.add_error('username', "Username is taken.")
        elif User.objects.filter(email=input.get('email')).exists():
            self.add_error('username', "Email is already in use.")
        elif " " in input.get('username'):
            self.add_error('username', "Usernames cannot contain spaces")
        elif "@" in input.get('username'):
            self.add_error('username', "Usernames cannot contain @ symbols")
        if password:
            if input.get('password') != input.get('vpassword'):
                self.add_error('password', 'Passwords do not match.')
            if len(password) < 8:
                self.add_error('password', 'Password must be 8 characters or more.')

        return input
