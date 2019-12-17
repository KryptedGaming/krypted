# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.apps import apps
from django.db.models import Q
# LOCAL IMPORTS
from .models import *
# EXTERNAL IMPORTS
# MISC
import logging, datetime

logger = logging.getLogger(__name__)

@login_required
@permission_required('applications.view_application', raise_exception=True)
def view_applications(request):
    return render(request, 'applications/view_applications.html', context= {
        'applications': Application.objects.all()})

@login_required
def view_my_applications(request):
    context = {}
    context['user_applications'] = Application.objects.filter(request_user=request.user)
    # build list of templates based on required groups or existing user applications
    application_templates = ApplicationTemplate.objects.filter(Q(required_group=None) | 
        Q(required_group__in=request.user.groups.all()) | 
        Q(pk__in=[application.template.pk for application in context['user_applications']]))

    application_template_response = []
    for application_template in application_templates:
        if Application.objects.filter(template=application_template, request_user=request.user).exists():
            application_template_response.append({
                "template": application_template,
                "in_progress": True, 
                "application": Application.objects.get(template=application_template, request_user=request.user)})

        else:
            application_template_response.append({
                "template": application_template,
                "in_progress": False, 
                "application": None})

    context['application_templates'] = application_template_response
    return render(request, 'applications/my_applications.html', context=context)

@login_required
@permission_required('applications.view_application', raise_exception=True)
def view_application(request, pk):
    context = {
        'application': Application.objects.get(pk=pk),
        'responses': ApplicationResponse.objects.filter(application_id=pk)
        }
    return render(request, 'applications/view_application.html', context)

@login_required
def create_application(request, template_id):
    context = {}

    if request.POST:
        application = Application(
                template=ApplicationTemplate.objects.get(pk=template_id),
                request_user = request.user,
                status = "PENDING",
                )
        application.save()

        # Build responses
        for question in application.template.questions.all():
            response = ApplicationResponse(question=question, application=application)
            response.response = request.POST.get("question_%s" % question.pk, "Response was not provided.")
            response.save()

        return redirect('my-applications')

    template = ApplicationTemplate.objects.get(pk=template_id)
    context['template'] = template
    return render(request, 'applications/create_application.html', context)

@login_required
def modify_application(request, application_id):
    context = {}
    application = Application.objects.get(pk=application_id)

    if request.POST:
        # Build responses
        print(request.POST)
        for response in ApplicationResponse.objects.filter(application=application):
            print(request.POST.get("question_%s" % response.question.pk))
            response.response = request.POST.get("question_%s" % response.question.pk, "Response was not provided.")
            response.save()

        return redirect('my-applications')

    context['template'] = application.template
    context['questions'] = []
    for response in ApplicationResponse.objects.filter(application=application):
        context['questions'].append({
            "question": response.question,
            "response": response, 
        })
    return render(request, 'applications/modify_application.html', context)

@login_required
@permission_required('applications.change_application', raise_exception=True)
def approve_application(request, application_id):
    application = Application.objects.get(pk=application_id)
    messages.add_message(request, messages.SUCCESS, 'Application accepted.')
    application.status = "ACCEPTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()
    application.save()

    for group in application.template.groups_to_add.all():
        if group not in application.request_user.groups.all():
            application.request_user.groups.add(group)
    
    for group in application.template.groups_to_remove.all():
        if group in application.request_user.groups.all():
            application.request_user.groups.remove(group)

    return redirect('application-list')

@login_required
@permission_required('applications.change_application', raise_exception=True)
def deny_application(request, application_id):
    application = Application.objects.get(pk=application_id)
    messages.add_message(request, messages.ERROR, 'Application rejected.')
    application.status = "REJECTED"
    application.response_user = request.user
    application.response_date = datetime.datetime.utcnow()

    for group in application.template.groups_to_add.all():
        if group in application.request_user.groups.all():
            application.request_user.groups.remove(group)

    for group in application.template.groups_to_remove.all():
        if group in application.request_user.groups.all():
            application.request_user.groups.remove(group)

    application.save()

    return redirect('application-list')

@login_required
@permission_required('applications.change_application', raise_exception=True)
def assign_application_to_user(request, application_id):
    application = Application.objects.get(pk=application_id)
    application.response_user = request.user
    application.status = "PENDING"
    application.save()
    return redirect('application-list')