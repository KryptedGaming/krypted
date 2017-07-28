from django.conf.urls import include, url
from django.contrib import admin
from hrapplications.views import hrapplications

# Create your views here.
## BASE
urlpatterns = [
    url(r'^$', hrapplications.dashboard, name='hr-dashboard'),
    url(r'^view/$', hrapplications.view_applications, name='hr-view-applications'),
    url(r'^process/$', hrapplications.process_applications, name='hr-view-applications'),
]

## APPLICATIONS
urlpatterns += [
    url(r'^create/(?P<slug>\w+)/$', hrapplications.create_application, name='hr-create-application'),
    url(r'^modify/(?P<slug>\w+)/$', hrapplications.modify_application, name='hr-modify-application'),
    url(r'^delete/(?P<slug>\w+)/$', hrapplications.delete_application, name='hr-delete-application'),
]
