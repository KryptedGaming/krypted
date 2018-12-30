# DJANGO IMPORTS
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
# LOCAL IMPORTS
from core.models import Survey, Guild
from core.decorators import login_required, permission_required
# MISC
from datetime import datetime

@login_required
@permission_required('core.view_survey')
def dashboard(request):
    surveys = Survey.objects.all();
    guilds = set([survey.guild for survey in surveys if survey is not None])
    context = {
        'surveys' : surveys,
        'guilds' : guilds
    }
    return render(request, 'base/surveys.html', context)

@login_required
@permission_required('core.view_survey')
def view_survey(request,pk):
    context = {}
    context['survey'] = Survey.objects.get(pk=pk)
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
