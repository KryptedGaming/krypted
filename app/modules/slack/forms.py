from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group

class SlackChannelForm(forms.Form):
    name = forms.CharField(max_length=16)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
