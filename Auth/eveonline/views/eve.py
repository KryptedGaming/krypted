from django.shortcuts import render
from eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Guild
from core.decorators import login_required
from core.views.base import get_global_context

# Create your views here.
@login_required
def dashboard(request):
    context = get_global_context(request)
    context = get_eve_context(request, context)
    return render(request, 'eve/dashboard.html', context)

def get_eve_context(request, context):
    user = request.user
    context['characters'] = EveCharacter.objects.filter(user=user)
    return context
