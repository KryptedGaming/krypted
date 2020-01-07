from django.shortcuts import render, redirect, get_object_or_404
from .models import Application 
from .helpers import get_manageable_application_templates
from django.contrib import messages

def user_can_manage_application(function):
    def wrap(request, *args, **kwargs):
        try:
            application = Application.objects.get(pk=kwargs['application_id'])
        except Exception as e:
            application = Application.objects.get(pk=kwargs['pk'])
        if application.template not in get_manageable_application_templates(request.user):
            messages.warning(request, "You cannot manage that application, it requires a particular group.")
            return redirect('application-list')
        return function(request, *args, **kwargs)
    return wrap 