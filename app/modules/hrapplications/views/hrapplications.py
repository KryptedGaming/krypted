from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from core.decorators import login_required
from core.models import Profile, Notification, Game, Event, Guild
from core.views.base import get_global_context
from modules.hrapplications.models import ApplicationTemplate, Application, Question, Response, Comment
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
    hrgroup, result = Group.objects.get_or_create(name='HR')
    if application.template.guild.group in request.user.groups.all() and hrgroup in request.user.groups.all():
        context['admin'] = True
    else:
        context['admin'] = False
    context['application'] = application
    context['responses'] = responses
    return render(request, 'hrapplications/view_application.html', context)

@login_required
def create_application(request, slug):
    logger.info(str(request.user) + " has requested to create an application for: " + str(slug))
    context = get_global_context(request)
    if request.POST:
        if Application.objects.filter(user=request.user, template__name=slug).exists():
            return redirect('hr-view-applications')
        logger.info(str(request.POST))
        application = Application(
                template=ApplicationTemplate.objects.get(name=slug),
                user = request.user,
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
                template = ApplicationTemplate.objects.get(name='eve')
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
        return render(request, 'hrapplications/create_application.html', context)

@login_required
def modify_application(request, slug):
    context = get_global_context(request)
    return render(request, 'hrapplications/dashboard.html', context)

@login_required
def delete_application(request, slug):
    context = get_global_context(request)
    return render(request, 'hrapplications/dashboard.html', context)
