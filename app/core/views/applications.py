# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
# LOCAL IMPORTS
from app.conf import discord as discord_settings
from core.decorators import login_required, permission_required, services_required
from core.models import *
# EXTERNAL IMPORTS
from games.eveonline.models import *
from modules.discord.models import DiscordUser
from modules.discord.tasks import send_discord_message
# MISC
import logging, datetime

logger = logging.getLogger(__name__)

@login_required
@services_required
@permission_required('core.manage_guild_applications')
def dashboard(request):
    context = {'applications': GuildApplication.objects.all()}
    return render(request, 'base/applications.html', context)

@login_required
@permission_required('core.manage_guild_applications')
def view_application(request, pk):
    context = {
        'application': GuildApplication.objects.get(pk=pk),
        'responses': GuildApplicationResponse.objects.filter(application_id=pk),
    }
    return render(request, 'applications/view_application.html', context)

@login_required
def add_application(request, slug):
    context = {}
    if slug == 'eve':
        if request.user.eve_characters.count() < 1:
            messages.add_message(request, messages.WARNING, 'Please add all of your EVE characters, then click apply.')
            return redirect('eve-dashboard')

    if request.POST:
        notify_user(user=request.user, slug=slug, type="submit")
        notify_recruitment_channel(request.user, slug, type="submit")
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
@permission_required('core.manage_guild_applications')
def approve_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "ACCEPTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if application.request_user.discord:
        notify_user(user=application.request_user, slug=application.template.guild.slug, type="accepted")
    application.request_user.guilds.add(application.template.guild)
    application.save()
    return redirect('hr-view-applications')

@login_required
@permission_required('core.manage_guild_applications')
def deny_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.WARNING, 'Application rejected.')
    application.status = "REJECTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    if application.request_user.discord:
        notify_user(user=application.request_user, slug=application.template.guild.slug, type="rejected")
    application.request_user.guilds.add(application.template.guild)
    application.save()
    return redirect('hr-view-applications')

@login_required
@permission_required('core.manage_guild_applications')
def assign_application(request, application, user):
    application = GuildApplication.objects.get(pk=application)
    application.response_user = request.user
    application.status = "PENDING"
    if application.request_user.discord:
        notify_user(user=application.request_user, slug=application.template.guild.slug, type="assigned", recruiter=request.user)
    # notify_applicant_recruiter_assignment(application.user, application.template.guild.slug, user)
    application.save()
    return redirect('hr-view-applications')

# HELPER FUNCTIONS
def notify_user(user, slug, type, **kwargs):
    if type == "submit":
        send_discord_message(
        discord_settings.RECRUITMENT_CHANNEL,
        "Thank you for submitting your %s application. Please wait up to 48 hours to be assigned a recruiter." % Guild.objects.get(slug=slug).name,
        user=user.id
        )
    elif type == "accepted":
        send_discord_message(
        discord_settings.RECRUITMENT_CHANNEL,
        "Congratulations, your application to %s has been **ACCEPTED.** Welcome aboard, DM your recruiter for the next step." % Guild.objects.get(slug=slug).name,
        user=user.id
        )
    elif type == "rejected":
        send_discord_message(
        discord_settings.RECRUITMENT_CHANNEL,
        "Sorry, your application to %s has been **REJECTED.** DM your recruiter for details." % Guild.objects.get(slug=slug).name,
        user=user.id
        )
    elif type == "assigned":
        recruiter = kwargs.get('recruiter')
        send_discord_message(
        discord_settings.RECRUITMENT_CHANNEL,
        "Your application to %s has been assigned to **%s**. DM them if you have questions." % (Guild.objects.get(slug=slug).name, recruiter.discord),
        user=user.id
        )



def notify_recruitment_channel(user, slug, type):
    if type == "submit":
        send_discord_message(
        discord_settings.HR_CHANNEL,
        "%s has submitted an %s application. Please add a :white_check_mark: if you intend on handling it." % (user.discord, Guild.objects.get(slug=slug).name),
        group=Guild.objects.get(slug=slug).group.id
        )
