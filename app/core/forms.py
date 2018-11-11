from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from core.models import User
import logging

logger = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)

    def clean(self):
        input = self.cleaned_data
        username = self.resolve_username(input.get('username'))

        if not authenticate(username=username, password=input.get('password')):
            self.add_error('username', 'Invalid credentials.')

        return input

    def resolve_username(self, username):
        email_valid = User.objects.filter(email=username).exists()
        if email_valid:
            return User.objects.get(email=username).username
        else:
            return username

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    email = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=32, required=True)
    vpassword = forms.CharField(max_length=32, required=True)
    region = forms.CharField(max_length=2, required=True)

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

class CoreAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass

class EventForm(forms.Form):
    pass

class ProfileForm(forms.Form):
    pass

class NotificationForm(forms.Form):
    pass

class GameForm(forms.Form):
    pass
