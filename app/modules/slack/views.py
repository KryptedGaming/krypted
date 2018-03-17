from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from modules.slack.tasks import add_slack_user
from django.conf import settings

# Create your views here.
def resend(request):
    if Group.objects.get(name=settings.EVE_ONLINE_GROUP) in request.user.groups.all():
        add_slack_user(request.user.pk)
        messages.add_message(request, messages.SUCCESS, 'Slack invite sent to %s. Check your email.' % request.user.email)
    else:
        messages.add_message(request, messages.SUCCESS, 'You need to be in the EVE group to join Slack.')
    return redirect('dashboard')

