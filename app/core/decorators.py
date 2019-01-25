from django.shortcuts import redirect
from django.contrib import messages
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
    def wrapper(request, *args, **kw):
        if request.user.discord and request.user.discourse:
            return function(request, *args, **kw)
        else:
            messages.add_message(request, messages.WARNING, 'Please set up your services before proceeding.')
            return redirect('dashboard')
    return wrapper
