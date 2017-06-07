from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', context={})

def login(request):
    return render(request, 'accounts/login.html', context={})

def register(request):
    return render(request, 'accounts/register.html', context={})

def logout(request):
    return redirect('/redirect/?page=login')
