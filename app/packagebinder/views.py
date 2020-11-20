from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib import messages
from django_celery_beat.models import PeriodicTask
from django.http import HttpResponse
from django.apps import apps

def setup(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    app_config = apps.get_app_config('packagebinder')
    for binding in app_config.settings_bindings:
        binding.refresh()
    for binding in app_config.task_bindings:
        binding.refresh()
    context = {
        "package_bindings": app_config.package_bindings,
        "settings_bindings": app_config.settings_bindings,
        "task_bindings": app_config.task_bindings
    }
    return render(request, "packagebinder/setup.html", context=context)

def enable_task(request):
    if 'task_id' not in request.GET:
        return HttpResponse(status=400)
    else:
        pk = request.GET['task_id']
    if not request.user.is_superuser:
        raise PermissionDenied()
    task = PeriodicTask.objects.get(pk=pk)
    task.enabled = True
    task.save()
    return HttpResponse(status=200)


def disable_task(request):
    if 'task_id' not in request.GET:
        return HttpResponse(status=400)
    else:
        pk = request.GET['task_id']
    if not request.user.is_superuser:
        raise PermissionDenied()
    task = PeriodicTask.objects.get(pk=pk)
    task.enabled = False
    task.save()
    return HttpResponse(status=200)

def update_package_settings(request, package_name):
    app_config = apps.get_app_config('packagebinder')
    settings_binding = None 
    for binding in app_config.settings_bindings:
        if binding.package_name == package_name:
            settings_binding = binding 
    if not settings_binding:
        raise ObjectDoesNotExist()
    if not request.user.is_superuser:
        raise PermissionDenied()
    try:
        request_data = request.POST.copy()
        form = binding.settings_form(request_data)
        if form.is_valid():
            messages.info(request, "Package settings were updated.")
            form.save()
        else:
            messages.error(request, "Failed to update package settings, some values supplied were invalid.")
    except Exception as e:
        messages.error(request, "Failed to update package settings.")
    
    return redirect('app-setup')