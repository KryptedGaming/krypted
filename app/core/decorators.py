from django.shortcuts import redirect
from django.contrib import messages
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated:
            logger.info("%s not authenticated, sending to login screen." % str(request.user))
            return redirect('/login/?next=' + request.path)
        else:
            return function(request, *args, **kw)
    return wrapper

def permission_required(permission, next='dashboard'):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                messages.add_message(request, messages.WARNING, 'You do not have permission to view that. Missing: %s' % permission)
                logger.info("%s attempted illegal action. Missing %s, sending to %s" % (str(request.user), permission, next))
                return redirect(next)
            else:
                return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def services_required(function):
    def wrapper(request, *args, **kwargs):
        if apps.is_installed("modules.discord") and not request.user.info.discord:
            messages.add_message(request, messages.WARNING, 'Please set up Discord before proceeding.')
            return redirect('dashboard')
        if apps.is_installed("modules.discourse") and not request.user.info.discourse:
            messages.add_message(request, messages.WARNING, 'Please set up your Forum account before proceeding.')
            return redirect('dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrapper
