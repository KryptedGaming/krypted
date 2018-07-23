from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib import messages
from core.decorators import login_required, permission_required
from core.models import Profile, Notification, Game, Event, Guild
from core.views.base import get_global_context
from modules.hrapplications.models import ApplicationTemplate, Application, Question, Response, Comment
from modules.hrapplications.decorators import services_required, eve_characters_required
from modules.discord.models import DiscordUser
from modules.discord.tasks import send_discord_message
from games.eveonline.models import *
import logging, datetime
logger = logging.getLogger(__name__)

## BASE
@login_required
def dashboard(request):
    context = get_global_context(request)
    applications = Application.objects.filter(user=request.user)
    context['applications'] = applications
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
@permission_required('hrapplications.view_application')
def view_application(request, pk):
    context = get_global_context(request)
    application = Application.objects.get(pk=pk)
    responses = Response.objects.filter(application=application)
    context['characters'] = EveCharacter.objects.filter(user=application.user)
    context['application'] = application
    context['responses'] = responses
    context['approve'] = request.user.has_perm('hrapplications.approve_application')
    context['deny'] = request.user.has_perm('hrapplications.deny_application')
    return render(request, 'hrapplications/view_application.html', context)

@login_required
@permission_required('hrapplications.view_applications')
def view_applications_all(request):
    context = get_global_context(request)
    context['applications'] = Application.objects.all()
    # Check if user has permission to admin applications
    return render(request, 'hrapplications/view_applications_all.html', context)

@login_required
@services_required
@eve_characters_required
def add_eve_application(request, slug='eve'):
    context = get_global_context(request)
    if request.POST:
        # if Application.objects.filter(user=request.user, template__guild__slug=slug).exists():
        #     return redirect('hr-change-application', id=Application.objects.get(user=request.user, template__slug=slug).id)
        notify_recruitment_channel(request.user, slug)
        application = Application(
                template=ApplicationTemplate.objects.get(guild=Guild.objects.get(slug=slug)),
                user = request.user,
                profile = Profile.objects.get(user=request.user),
                status = "Pending",
                reviewer = None,
                )
        application.save()

        # Build responses
        for question in application.template.questions.all():
            response = Response(question=question, application=application)
            response.response = request.POST.get(str(question.pk), "Response was not provided.")
            response.save()
        return redirect('dashboard')
    else:
        if Application.objects.filter(user=request.user, template__guild__slug=slug).exists():
            return redirect('hr-change-application', id=Application.objects.get(user=request.user, template__guild__slug=slug).id)
        try:
            template = ApplicationTemplate.objects.get(guild=Guild.objects.get(title="EVE Online"))
            characters = EveCharacter.objects.filter(user=request.user)
            context['characters'] = characters
        except:
            logger.info("FIXTURE ERROR: No EVE template for applications.")

        context['template'] = template
        return render(request, 'hrapplications/application_base.html', context)

@login_required
@services_required
def add_application(request, slug):
    context = get_global_context(request)
    if request.POST:
        notify_recruitment_channel(request.user, slug)
        application = Application(
                template=ApplicationTemplate.objects.get(guild=Guild.objects.get(slug=slug)),
                user = request.user,
                profile = Profile.objects.get(user=request.user),
                status = "Pending",
                reviewer = None,
                )
        application.save()

        # Build responses
        for question in application.template.questions.all():
            response = Response(question=question, application=application)
            response.response = request.POST.get(str(question.pk), "Response was not provided.")
            response.save()
        return redirect('dashboard')
    else:
        if Application.objects.filter(user=request.user, template__guild__slug=slug).exists():
            return redirect('hr-change-application', id=Application.objects.get(user=request.user, template__guild__slug=slug).id)
        template = ApplicationTemplate.objects.get(guild__slug=slug)
        context['template'] = template
    return render(request, 'hrapplications/application_base.html', context)

@login_required
def change_application(request, id):
    context = get_global_context(request)
    application = Application.objects.get(pk=id)
    if request.POST:
        for question in application.template.questions.all():
            response = Response(question=question, application=application)
            response.response = request.POST.get(str(question.pk), "Response was not provided.")
            response.save()
        return redirect('dashboard')
    else:
        context['template'] = application.template
        context['application'] = application
    return render(request, 'hrapplications/application_base.html', context)

@login_required
def delete_application(request, slug):
    context = get_global_context(request)
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
def add_application_comment(request, application):
    pass

@login_required
@permission_required('hrapplications.approve_application')
def approve_application(request, application):
    application = Application.objects.get(pk=application)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "Approved"
    application.processed_date = datetime.datetime.utcnow()
    notify_applicant_decision(application.user, slug=application.template.guild.slug, decision="ACCEPTED")
    Profile.objects.get(user=application.user).guilds.add(application.template.guild)
    application.save()
    return redirect('hr-view-applications-all')

@login_required
@permission_required('hrapplications.deny_application')
def deny_application(request, application):
    application = Application.objects.get(pk=application)
    messages.add_message(request, messages.WARNING, 'Application rejected.')
    application.status = "Rejected"
    notify_applicant_decision(application.user, slug=application.template.guild.slug, decision="REJECTED")
    application.save()
    return redirect('hr-view-applications-all')

@login_required
def assign_application(request, application, user):
    application = Application.objects.get(pk=application)
    user = User.objects.get(pk=user)
    application.reviewer = user
    application.status = "Processing"
    notify_applicant_recruiter_assignment(application.user, application.template.guild.slug, user)
    application.save()
    return redirect('hr-view-applications-all')

# HELPER FUNCTIONS
def notify_recruitment_channel(user, slug):
    try:
        guild_applying_to = Guild.objects.get(slug=slug)
        user_discord_user = DiscordUser.objects.get(user=user)
        if slug == 'eve':
            user_eve_character = EveCharacter.objects.get(user=user, main=None)
            message = "@%s has created an application to join EVE Online. @here" % user_discord_user.username
            channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
            send_discord_message(channel, message)
        elif slug == 'wow':
            message = "@%s has created an application to join World of Warcraft. @here" % user_discord_user.username
            channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
            send_discord_message(channel, message)
        else:
            message = "@%s has created an application to join %s." % (user_discord_user.username, guild_applying_to.title)
            channel = settings.DISCORD_CHANNEL_IDS['#hr-manager']
            send_discord_message(channel, message)

    except Exception as e:
        logger.error("Fatal error in notify_recruitment_channel(). %s" % e)

def notify_applicant_decision(user, slug, decision):
    try:
        guild_applying_to = Guild.objects.get(slug=slug)
        user_discord_user = DiscordUser.objects.get(user=user)
        channel = settings.DISCORD_CHANNEL_IDS['#recruitment']
        message = "<@%s>, your application to %s has been **%s**." % (user_discord_user.id, guild_applying_to.title, decision)
        send_discord_message(channel, message)
    except Exception as e:
        logger.error("Fatal error in notify_applicant_decision(). %s" % e)

def notify_applicant_recruiter_assignment(user, slug, recruiter):
    try:
        guild_applying_to = Guild.objects.get(slug=slug)
        user_discord_user = DiscordUser.objects.get(user=user)
        recruiter_discord_user = DiscordUser.objects.get(user=recruiter)
        message = "<@%s>, your application to %s has been assigned to Recruiter <@%s>." % (user_discord_user.id, guild_applying_to.title, recruiter_discord_user.id)
        channel = settings.DISCORD_CHANNEL_IDS['#recruitment']
        send_discord_message(channel, message)
    except Exception as e:
        logger.error("Fatal error in notify_applicant_recruiter_assignment(). %s" % e)
