# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


@login_required
def dashboard(request):
    return redirect('accounts-user', username=request.user.username)
    
def handler500(request):
    return render(request, '500.html', status=505)
