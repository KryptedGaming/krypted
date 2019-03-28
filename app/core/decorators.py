from django.shortcuts import redirect
from django.contrib import messages
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


def new_user(function):
    def wrapper(request, *args, **kwargs):
        if 'new_user' in request.session:
            return redirect('tutorial')
        else:
            return function(request, *args, **kwargs)
    return wrapper

def services_required(function):
    def wrapper(request, *args, **kwargs):
        # check for services
        if not request.user.is_authenticated:
            logger.info("%s not authenticated, sending to login screen." % str(request.user))
            return redirect('/login/?next=' + request.path)
        elif apps.is_installed("modules.discord") and not request.user.info.discord:
            messages.add_message(request, messages.WARNING, 'Please set up Discord before proceeding.')
            if 'new_user' in request.session:
                return redirect('tutorial')
            return redirect('dashboard')
        elif apps.is_installed("modules.discourse") and not request.user.info.discourse:
            messages.add_message(request, messages.WARNING, 'Please set up your Forum account before proceeding.')
            if 'new_user' in request.session:
                return redirect('tutorial')
            return redirect('dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrapper

