from django import forms
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from accounts.utilities import send_activation_email, username_or_email_resolver
from accounts.models import UserInfo
import logging
import re
logger = logging.getLogger(__name__)


class UserRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=32, required=True)
    password = forms.CharField(min_length=8, max_length=32, required=True)
    v_password = forms.CharField(required=True, label="Verify Password")
    email = forms.CharField(max_length=64, required=True)
    country = CountryField().formfield(required=True)
    age = forms.IntegerField(required=True)

    def clean(self):
        # Display error for existing usersnames
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            self.add_error('username', 'Username is already taken')
        # Display errors for existing emails
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            self.add_error('email', 'Email is already taken')
        # Display errors for usernames with spaces
        if " " in str(self.cleaned_data.get('username')):
            self.add_error('username',
                           "Usernames cannot contain spaces")
        # Display errors for usernames that are emails
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if regex.search(str(self.cleaned_data.get('username'))):
            self.add_error('username',
                           "Usernames cannot contain special characters")
        # Display errors for mismatched passwords
        if self.cleaned_data.get('password') != self.cleaned_data.get('v_password'):
            self.add_error('password', 'Passwords do not match')
        # Display errors for underage users
        if self.cleaned_data.get('age') < 18:
            self.add_error('age', 'Sorry, you must be 18 or older to sign in.')

        return self.cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=32, required=True)
    password = forms.CharField(min_length=8, max_length=32, required=True)

    def clean(self):
        username = self.cleaned_data['username']
        username = username_or_email_resolver(username)
        password = self.cleaned_data['password']

        # checks
        user_exists = User.objects.filter(username=username).exists()
        user_authenticated = authenticate(username=username, password=password)
        if user_exists:
            user = User.objects.get(username=username)
            user_info = UserInfo.objects.get_or_create(user=user)
            user_active = user.is_active

        # authenticate check
        if not user_exists:
            self.add_error('username', 'User does not exist.')
            return self.cleaned_data
        if not user_authenticated:
            self.add_error('password', 'Invalid credentials.')
        if user_exists and not user_active:
            send_activation_email(User.objects.get(username=username))
            self.add_error(
                'username', 'Account not active, please check your email or reset password')

        return self.cleaned_data


class UserUpdateForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=32, required=False)
    email = forms.CharField(max_length=64, required=False)

    def clean(self):
        # Display error for existing usersnames
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            self.add_error('username', 'Username is already taken')
        # Display errors for existing emails
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            self.add_error('email', 'Email is already taken')
        # Display errors for usernames with spaces
        if " " in str(self.cleaned_data.get('username')):
            self.add_error('username',
                           "Usernames cannot contain spaces")
        # Display errors for usernames that are emails
        if "@" in str(self.cleaned_data.get('username')):
            self.add_error('username',
                           "Usernames cannot contain @ symbols")

        return self.cleaned_data
