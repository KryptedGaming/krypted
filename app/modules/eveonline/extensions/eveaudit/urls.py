from django.conf.urls import include, url
from modules.eveonline.extensions.eveaudit import views 
from django.contrib import messages

urlpatterns = [
    url(r'^character/update/(?P<character>\w+)/$', views.update_eve_character, name='eveaudit-update-character'),
]
