# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.apps import apps
# LOCAL IMPORTS
from modules.guilds.models import *
# EXTERNAL IMPORTS
# MISC
import logging, datetime

logger = logging.getLogger(__name__)

@login_required
@permission_required('guilds.manage_guild_applications')
def dashboard(request):
    context = {'applications': GuildApplication.objects.all()}
    return render(request, 'applications/applications.html', context)

@login_required
@permission_required('guilds.manage_guild_applications')
def view_application(request, pk):
    context = {
        'application': GuildApplication.objects.get(pk=pk),
        'responses': GuildApplicationResponse.objects.filter(application_id=pk),
    }
    return render(request, 'applications/view_application.html', context)

@login_required
def add_application(request, slug):
    context = {}
    if slug == 'eve' and apps.is_installed("modules.eveonline"):
        if request.user.info.eve_characters.count() < 1:
            messages.add_message(request, messages.WARNING, 'Please add all of your EVE characters, then click apply.')
            return redirect('eve-dashboard')

    if request.POST:
        if apps.is_installed('modules.discord'):
            from modules.guilds.integrations import discord_notify_user, discord_notify_recruitment_channel
            discord_notify_user(user=request.user, slug=slug, type="submit")
            discord_notify_recruitment_channel(request.user, slug, type="submit")

        application = GuildApplication(
                template=GuildApplicationTemplate.objects.get(guild=Guild.objects.get(slug=slug)),
                request_user = request.user,
                status = "PENDING",
                )
        application.save()

        # Build responses
        for question in application.template.questions.all():
            response = GuildApplicationResponse(question=question, application=application)
            response.response = request.POST.get(str(question.pk), "Response was not provided.")
            response.save()

        return redirect('dashboard')

    template = GuildApplicationTemplate.objects.get(guild=Guild.objects.get(slug=slug))
    context['template'] = template
    return render(request, 'applications/application_base.html', context)

@login_required
@permission_required('guilds.manage_guild_applications')
def approve_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "ACCEPTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if apps.is_installed('modules.discord'):
        from modules.guilds.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, slug=application.template.guild.slug, type="accepted")
    if apps.is_installed('modules.guilds'):
        application.template.guild.users.add(application.request_user)
    application.save()
    return redirect('hr-view-applications')

@login_required
@permission_required('guilds.manage_guild_applications')
def deny_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.ERROR, 'Application rejected.')
    application.status = "REJECTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if apps.is_installed('modules.discord'):
        from modules.guilds.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, slug=application.template.guild.slug, type="rejected")
    if apps.is_installed('modules.guilds'):
        if request.user in application.template.guild.users.all():
            application.template.guild.users.remove(application.request_user)
    application.save()
    return redirect('hr-view-applications')

@login_required
@permission_required('guilds.manage_guild_applications')
def assign_application(request, application, user):
    application = GuildApplication.objects.get(pk=application)
    application.response_user = request.user
    application.status = "PENDING"
    if apps.is_installed('modules.discord'):
        from modules.guilds.integrations import discord_notify_user
        if application.request_user.info.discord:
            discord_notify_user(user=application.request_user, slug=application.template.guild.slug, type="assigned", recruiter=request.user)
    # notify_applicant_recruiter_assignment(application.user, application.template.guild.slug, user)
    application.save()
    return redirect('hr-view-applications')
