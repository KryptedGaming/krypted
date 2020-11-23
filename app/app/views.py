# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.conf import settings
from notifications.models import Notification
import json

@login_required
def dashboard(request):
    if 'django_eveonline_connector' in settings.INSTALLED_APPS:
        from django_eveonline_connector.models import PrimaryEveCharacterAssociation
        if request.user.eve_tokens.all().count() > 1 and not PrimaryEveCharacterAssociation.objects.filter(user=request.user).exists():
            messages.warning(request, "You need to select a primary EVE Online character.")
            return redirect('django-eveonline-connector-character-select-primary')
    return redirect('accounts-user', username=request.user.username)
    
def handler500(request):
    return render(request, '500.html', status=505)

@login_required
def unread_notifications(request):
    import logging 
    logger = logging.getLogger(__name__)
    from django.http import JsonResponse
    return JsonResponse({ "data": [
        {
            "timestamp": f"{notification.timesince()} ago",
            "verb": notification.verb,
            "action": """
            <div class="btn-group btn-block">
                <button type="button" class="btn btn-info" data-toggle="modal" data-target="#modal-%s">
                  View Details
                </button>
                <button class="btn btn-success">Mark as Read</button>
            </div>
            <div class="modal fade" id="modal-%s" style="padding-right: 17px;" aria-modal="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h4 class="modal-title">Description</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                    </div>
                    <div class="modal-body">
                    <p>%s</p>
                    </div>
                    <div class="modal-footer justify-content-between">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    </div>
                </div>
                <!-- /.modal-content -->
                </div>
                <!-- /.modal-dialog -->
            </div>
            """ % (notification.pk, notification.pk, notification.description)
        }
        for notification
        in request.user.notifications.unread().exclude(public=False)
    ]}, safe=False)

@login_required
def unread_system_notifications(request):
    from django.http import JsonResponse
    return JsonResponse({ "data": [
        {
            "timestamp": f"{notification.timesince()} ago",
            "verb": notification.verb,
            "action": """
            <div class="btn-group btn-block">
                <button type="button" class="btn btn-info" data-toggle="modal" data-target="#modal-%s">
                  View Details
                </button>
                <button class="btn btn-success">Mark as Read</button>
            </div>
            <div class="modal fade" id="modal-%s" style="padding-right: 17px;" aria-modal="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h4 class="modal-title">Description</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                    </div>
                    <div class="modal-body">
                    <pre>%s</pre>
                    </div>
                    <div class="modal-footer justify-content-between">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    </div>
                </div>
                <!-- /.modal-content -->
                </div>
                <!-- /.modal-dialog -->
            </div>
            """ % (notification.pk, notification.pk, notification.description)
        }
        for notification
        in request.user.notifications.unread().exclude(public=True)
    ]}, safe=False)

@login_required
def mark_as_read(request, notification_pk):
    if not Notification.objects.filter(pk=pk).exists():
        return HttpResponse(status=404)
    notification = Notification.objects.get(pk=notification_pk)
    if request.user != notification.recipient:
        return HttpResponse(status=403)
    
    notification.mark_as_read()
    return HttpResponse(status=200)