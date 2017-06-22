from django.shortcuts import render
from eveonline.models import Token, EveCharacter

# Create your views here.
def dashboard(request):
    return render(
    request,
    'eve/dashboard.html',
     context={
        }
    )
