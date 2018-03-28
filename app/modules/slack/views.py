from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from modules.slack.tasks import add_slack_user, get_slack_user
from modules.slack.tasks import add_slack_channel as task_add_slack_channel
from modules.slack.forms import *
from django.conf import settings
import logging
logger = logging.getLogger(__name__)



# Create your views here.
def resend(request):
    if Group.objects.get(name=settings.EVE_ONLINE_GROUP) in request.user.groups.all():
        add_slack_user.apply_async(args=[request.user.pk])
        get_slack_user.apply_async(args=[request.user.pk])
        messages.add_message(request, messages.SUCCESS, 'Slack invite sent to %s. Check your email.' % request.user.email)
    else:
        messages.add_message(request, messages.SUCCESS, 'You need to be in the EVE group to join Slack.')
    return redirect('dashboard')

def add_slack_channel(request):
    if request.method == 'POST':
        form = SlackChannelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            groups = [str(group.pk) for group in form.cleaned_data['groups']]
            task_add_slack_channel.apply_async(args=[name, "-".join(groups)])
            return redirect('dashboard')
    else:
        form = SlackChannelForm()
    return render(request, 'add_slack_channel.html', {'form': form})
