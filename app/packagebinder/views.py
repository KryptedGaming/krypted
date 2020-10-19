from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django_celery_beat.models import PeriodicTask
from django.http import HttpResponse
from django.apps import apps

def setup(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    bindings = apps.get_app_config('packagebinder').package_bindings
    for binding in bindings:
        binding.refresh()
    context = {
        "bindings": bindings
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
