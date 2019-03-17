from django.shortcuts import redirect
from django.contrib import messages
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

def services_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.info("%s not authenticated, sending to login screen." % str(request.user))
            return redirect('/login/?next=' + request.path)
        elif apps.is_installed("modules.discord") and not request.user.info.discord:
            messages.add_message(request, messages.WARNING, 'Please set up Discord before proceeding.')
            return redirect('dashboard')
        elif apps.is_installed("modules.discourse") and not request.user.info.discourse:
            messages.add_message(request, messages.WARNING, 'Please set up your Forum account before proceeding.')
            return redirect('dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrapper
