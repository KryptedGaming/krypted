from django.shortcuts import render
from eveonline.models import Token, EveCharacter
from django.contrib.auth.models import User, Group
from core.models import Guild

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated():
        user = request.user
        guild = Guild.objects.get(title="EVE Online")
        if guild.group in user.groups.all():
            member = True
            print("True")
        else:
            print("False")
            member = False
        return render(
        request,
        'eve/dashboard.html',
         context={
            'user': 'user',
            'member': member,
            }
        )
    else:
        return redirect('login')
