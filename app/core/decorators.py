from django.contrib.auth.models import User
from django.shortcuts import redirect

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            return function(request, *args, **kw)
    return wrapper
