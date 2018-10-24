from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.decorators import login_required, permission_required
from core.models import *
from games.eveonline.models import *
# from modules.discord.models import DiscordUser
# from modules.discord.tasks import send_discord_message
import logging, datetime
logger = logging.getLogger(__name__)

## BASE
@login_required
def dashboard(request):
    context = {}
    context['applications'] = GuildApplications.order_by(request_date)
    return render(request, 'applications/dashboard.html', context)

@login_required
@permission_required('core.manage_guild_applications')
def view_application(request, pk):
    context = {
        'application': GuildApplication.objects.get(pk=pk),
        'responses': GuildApplicationResponse.objects.filter(application_id=pk),
        'characters': EveCharacter.objects.filter(user=request.user),
    }
    return render(request, 'applications/view_application.html', context)

@login_required
def add_eve_application(request, slug='eve'):
    context = {}
    if request.POST:
        # notify_recruitment_channel(request.user, slug)
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

    template = GuildApplicationTemplate.objects.get(guild=Guild.objects.get(name="EVE Online"))
    context['template'] = template
    return render(request, 'applications/application_base.html', context)

@login_required
def add_application(request, slug):
    context = {}
    if request.POST:
        # notify_recruitment_channel(request.user, slug)
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

    template = GuildApplicationTemplate.objects.get(guild=Guild.objects.get(name="EVE Online"))
    context['template'] = template
    return render(request, 'applications/application_base.html', context)

@login_required
def approve_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "ACCEPTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    # notify_applicant_decision(application.user, slug=application.template.guild.slug, decision="ACCEPTED")
    application.request_user.guilds.add(application.template.guild)
    application.save()
    return redirect('hr-view-applications')

@login_required
def deny_application(request, application):
    application = GuildApplication.objects.get(pk=application)
    messages.add_message(request, messages.WARNING, 'Application rejected.')
    application.status = "REJECTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    # notify_applicant_decision(application.user, slug=application.template.guild.slug, decision="REJECTED")
    application.save()
    return redirect('hr-view-applications')

@login_required
def assign_application(request, application, user):
    application = GuildApplication.objects.get(pk=application)
    application.response_user = request.user
    application.status = "PENDING"
    # notify_applicant_recruiter_assignment(application.user, application.template.guild.slug, user)
    application.save()
    return redirect('hr-view-applications')

# HELPER FUNCTIONS
# def notify_recruitment_channel(user, slug):
#     try:
#         guild_applying_to = Guild.objects.get(slug=slug)
#         user_discord_user = DiscordUser.objects.get(user=user)
#         if slug == 'eve':
#             user_eve_character = EveCharacter.objects.get(user=user, main=None)
#             message = "@%s has created an application to join EVE Online. @here" % user_discord_user.username
#             channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
#             send_discord_message(channel, message)
#         elif slug == 'wow':
#             message = "@%s has created an application to join World of Warcraft. @here" % user_discord_user.username
#             channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
#             send_discord_message(channel, message)
#         else:
#             message = "@%s has created an application to join %s." % (user_discord_user.username, guild_applying_to.name)
#             channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
#             send_discord_message(channel, message)
#
#     except Exception as e:
#         logger.error("Fatal error in notify_recruitment_channel(). %s" % e)
#
# def notify_applicant_decision(user, slug, decision):
#     try:
#         guild_applying_to = Guild.objects.get(slug=slug)
#         user_discord_user = DiscordUser.objects.get(user=user)
#         channel = settings.DISCORD_CHANNEL_IDS['#recruitment']
#         message = "<@%s>, your application to %s has been **%s**." % (user_discord_user.id, guild_applying_to.name, decision)
#         send_discord_message(channel, message)
#     except Exception as e:
#         logger.error("Fatal error in notify_applicant_decision(). %s" % e)
#
# def notify_applicant_recruiter_assignment(user, slug, recruiter):
#     try:
#         guild_applying_to = Guild.objects.get(slug=slug)
#         user_discord_user = DiscordUser.objects.get(user=user)
#         recruiter_discord_user = DiscordUser.objects.get(user=recruiter)
#         message = "<@%s>, your application to %s has been assigned to Recruiter <@%s>." % (user_discord_user.id, guild_applying_to.name, recruiter_discord_user.id)
#         channel = settings.DISCORD_CHANNEL_IDS['#recruitment']
#         send_discord_message(channel, message)
#     except Exception as e:
#         logger.error("Fatal error in notify_applicant_recruiter_assignment(). %s" % e)
