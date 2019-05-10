# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.apps import apps
# INTERNAL IMPORTS
from modules.eveonline.extensions.evedoctrine.models import EveFitting, EveDoctrine
# MISC
import logging, time

eve_settings = apps.get_app_config('eveonline')
logger = logging.getLogger(__name__)

@login_required
@permission_required('evedoctrine.view_evedoctrine')
def doctrines(request):
    context = {}
    context['doctrines'] = EveDoctrine.objects.all()
    
    return render(request, 'evedoctrine/doctrines.html', context)

@login_required
@permission_required('evedoctrine.view_evedoctrine')
def view_doctrine(request, doctrine):
    context = {}
    context['doctrine'] = EveDoctrine.objects.get(pk=doctrine)
    context['groups'] = set()
    for fitting in context['doctrine'].fittings.all():
        context['groups'].add(fitting.group)
    return render(request, 'evedoctrine/view_doctrine.html', context)

@login_required
@permission_required('evedoctrine.view_evefitting')
def fittings(request):
    context = {} 
    context['fittings'] = EveFitting.objects.all()
    return render(request, 'evedoctrine/fittings.html', context)

@login_required
@permission_required('evedoctrine.view_evefitting')
def view_fitting(request, fitting):
    context = {} 
    context['fittings'] = EveFitting.objects.get(pk=fitting)
    return render(request, 'evedoctrine/view_fitting.html', context)