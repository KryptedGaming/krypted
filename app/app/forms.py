from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import logging
logger = logging.getLogger(__name__)


class UserRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=32, required=True)
    password = forms.CharField(min_length=8, max_length=32, required=True)
    v_password = forms.CharField(required=True, label="Verify Password")
    email = forms.CharField(max_length=64, required=True)
    country = CountryField().formfield()
    age = forms.IntegerField()

    def clean(self):
        # Display error for existing usersnames
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            self.add_error('username', 'Username is already taken')
        # Display errors for existing emails
        if User.objects.filter(username=self.cleaned_data.get('email')).exists():
            self.add_error('email', 'Email is already taken')
        # Display errors for usernames with spaces
        if " " in self.cleaned_data.get('username'):
            self.add_error('username',
                           "Usernames cannot contain spaces")
        # Display errors for usernames that are emails
        if "@" in self.cleaned_data.get('username'):
            self.add_error('username',
                           "Usernames cannot contain @ symbols")
        # Display errors for mismatched passwords
        if self.cleaned_data.get('password') != self.cleaned_data.get('v_password'):
            self.add_error('password', 'Passwords do not match')

        return self.cleaned_data
