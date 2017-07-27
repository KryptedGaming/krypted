from django.conf.urls import include, url
from django.contrib import admin
from hrapplications.views import hrapplications

# Create your views here.
## BASE
urlpatterns = [
    url(r'^$', hrapplications.dashboard, name='hr-dashboard'),
]
