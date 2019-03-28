# DJANGO IMPORTS
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
# EXTERNAL IMPORTS
from modules.engagement.models import Survey

@login_required
@permission_required('engagement.view_survey')
def dashboard(request):
    surveys = Survey.objects.all();
    groups = set([survey.group for survey in surveys if survey is not None])
    context = {
        'surveys' : surveys,
        'groups' : groups
    }
    return render(request, 'surveys/surveys.html', context)

@login_required
@permission_required('engagement.view_survey')
def view_survey(request,pk):
    context = {}
    s = Survey.objects.get(pk=pk)
    group_users = User.objects.filter(groups=s.group)
    context['survey'] = s
    context['survey_users_missing'] = set(group_users) - set(s.users_completed.all())
    context['total_users'] = len(group_users)
    return render(request, 'surveys/view_survey.html', context)

@login_required
def redirect_to_survey(request,pk):
    survey = Survey.objects.get(pk=pk)
    if not survey.is_expired:
        survey.users_started.add(request.user)
        return HttpResponseRedirect(survey.url)
    else:
        messages.error(request,"Survey has expired and is no longer valid")
        return redirect('/')

@login_required
def complete_survey(request,pk):
    survey = Survey.objects.get(pk=pk)
    if not survey.is_expired:
        if 'survey_key' in request.GET and request.GET['survey_key'] == survey.survey_key.__str__():
            survey.users_completed.add(request.user)
            messages.add_message(request,messages.SUCCESS,"Survey participation recorded")
        else:
            messages.error(request,"Invalid secret key for survey")
    else:
        messages.error(request,"Survey has expired and is no longer valid")
    return redirect('/')
