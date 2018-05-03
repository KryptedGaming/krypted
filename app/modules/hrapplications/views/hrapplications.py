from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event, Guild
from core.views.base import get_global_context
from modules.hrapplications.models import ApplicationTemplate, Application, Question, Response, Comment
from games.eveonline.models import *
import logging
logger = logging.getLogger(__name__)

## BASE
@login_required
def dashboard(request):
    context = get_global_context(request)
    applications = Application.objects.filter(user=request.user)
    context['applications'] = applications
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
def view_application(request, pk):
    context = get_global_context(request)
    application = Application.objects.get(pk=pk)
    responses = Response.objects.filter(application=application)
    logger.info(responses)
    # Check if user has permission to admin applications
    hrgroup, result = Group.objects.get_or_create(name=settings.HR_GROUP)
    if application.template.guild.group in request.user.groups.all() and hrgroup in request.user.groups.all():
        context['admin'] = True
    else:
        context['admin'] = False
    context['characters'] = EveCharacter.objects.filter(user=application.user)
    context['application'] = application
    context['responses'] = responses
    context['approve'] = request.user.has_perm('hrapplications.approve_application')
    context['deny'] = request.user.has_perm('hrapplications.deny_application')
    return render(request, 'hrapplications/view_application.html', context)

@login_required
def view_applications_all(request):
    context = get_global_context(request)
    context['applications'] = Application.objects.all()
    # Check if user has permission to admin applications
    if not request.user.has_perm('hrapplications.view_applications'):
        messages.add_message(request, messages.ERROR, 'You do not have permission to view that.')
        return redirect('dashboard')
    return render(request, 'hrapplications/view_applications_all.html', context)

@login_required
def create_application(request, slug):
    logger.info(str(request.user) + " has requested to create an application for: " + str(slug))
    context = get_global_context(request)
    if request.POST:
        if Application.objects.filter(user=request.user, template__name=slug).exists():
            return redirect('hr-view-applications')
        logger.info(str(request.POST))
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
        if slug == 'eve':
            try:
                template = ApplicationTemplate.objects.get(guild=Guild.objects.get(title="EVE Online"))
                characters = EveCharacter.objects.filter(user=request.user)
                context['characters'] = characters
            except:
                logger.info("FIXTURE ERROR: No EVE template for applications.")
        elif slug == 'albion':
            try:
                template = ApplicationTemplate.objects.get(name='albion')
            except:
                logger.info("FIXTURE ERROR: No Albion template for applications.")
        else:
            logger.info("ERROR : User requested a slug with no supported template." + str(slug))
        context['template'] = template
        return render(request, 'hrapplications/application_base.html', context)

@login_required
def modify_application(request, slug):
    context = get_global_context(request)
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
def delete_application(request, slug):
    context = get_global_context(request)
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
def add_application_comment(request, application):
    pass

@login_required
def approve_application(request, application):
    application = Application.objects.get(pk=application)
    if Group.objects.get(name=settings.HR_GROUP) in request.user.groups.all():
        messages.add_message(request, messages.SUCCESS, 'Application accepted.')
        application.status = "Approved"
        application.save()
    return redirect('hr-view-applications-all')

@login_required
def deny_application(request, application):
    application = Application.objects.get(pk=application)
    if Group.objects.get(name=settings.HR_GROUP) in request.user.groups.all():
        messages.add_message(request, messages.WARNING, 'Application rejected.')
        application.status = "Rejected"
        application.save()
    return redirect('hr-view-applications-all')

@login_required
def assign_application(request, application, user):
    application = Application.objects.get(pk=application)
    user = User.objects.get(pk=user)
    application.reviewer = user
    application.status = "Processing"
    application.save()
    return redirect('hr-view-applications-all')
