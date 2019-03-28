# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.apps import apps
# LOCAL IMPORTS
from modules.applications.models import *
# EXTERNAL IMPORTS
# MISC
import logging, datetime

logger = logging.getLogger(__name__)

@login_required
@permission_required('applications.change_application')
def dashboard(request):
    context = {'applications': Application.objects.all()}
    return render(request, 'applications/applications.html', context)

@login_required
@permission_required('applications.change_application')
def view_application(request, pk):
    context = {
        'application': Application.objects.get(pk=pk),
        'responses': ApplicationResponse.objects.filter(application_id=pk),
    }
    return render(request, 'applications/view_application.html', context)

@login_required
def add_application(request, group_id):
    context = {}

    if request.POST:
        if apps.is_installed('modules.discord'):
            from modules.applications.integrations import discord_notify_user, discord_notify_recruitment_channel
            discord_notify_user(user=request.user, group_id=group_id, type="submit")
            discord_notify_recruitment_channel(request.user, group_id=group_id, type="submit")

        application = Application(
                template=ApplicationTemplate.objects.get(group__id=group_id),
                request_user = request.user,
                status = "PENDING",
                )
        application.save()

        # Build responses
        for question in application.template.questions.all():
            response = ApplicationResponse(question=question, application=application)
            response.response = request.POST.get(str(question.pk), "Response was not provided.")
            response.save()

        return redirect('dashboard')

    template = ApplicationTemplate.objects.get(group__id=group_id)
    context['template'] = template
    return render(request, 'applications/application_base.html', context)

@login_required
@permission_required('applications.change_application')
def approve_application(request, application):
    application = Application.objects.get(pk=application)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "ACCEPTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if apps.is_installed('modules.discord'):
        from modules.applications.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, group_id=application.template.group.id, type="accepted")
    application.save()

    # if automated, add group
    if application.template.automated:
        application.request_user.groups.add(application.template.group)

    return redirect('view-applications')

@login_required
@permission_required('applications.change_application')
def deny_application(request, application):
    application = Application.objects.get(pk=application)
    messages.add_message(request, messages.ERROR, 'Application rejected.')
    application.status = "REJECTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if apps.is_installed('modules.discord'):
        from modules.applications.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, group_id=application.template.group.id, type="rejected")
    application.save()

    # if automated, remove group
    if application.template.automated:
        if application.template.group in application.request_user.groups.all():
            application.request_user.groups.remove(application.template.group)

    return redirect('view-applications')

@login_required
@permission_required('applications.change_guildapplication')
def assign_application(request, application, user):
    application = Application.objects.get(pk=application)
    application.response_user = request.user
    application.status = "PENDING"
    if apps.is_installed('modules.discord'):
        from modules.applications.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, group_id=application.template.group.id, type="assigned", recruiter=request.user)
    application.save()
    return redirect('view-applications')
