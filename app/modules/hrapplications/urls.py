from django.conf.urls import include, url
from django.contrib import admin
from modules.hrapplications.views import hrapplications

# Create your views here.
## BASE
urlpatterns = [
    url(r'^$', hrapplications.dashboard, name='hr-dashboard'),
]

## APPLICATIONS
urlpatterns += [
    url(r'^create/(?P<slug>\w+)/$', hrapplications.create_application, name='hr-create-application'),
    url(r'^modify/(?P<slug>\w+)/$', hrapplications.modify_application, name='hr-modify-application'),
    url(r'^delete/(?P<slug>\w+)/$', hrapplications.delete_application, name='hr-delete-application'),
    url(r'^view/(?P<pk>\w+)/$', hrapplications.view_application, name='hr-view-application'),
]
