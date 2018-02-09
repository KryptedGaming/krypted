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
    url(r'^view/$', hrapplications.view_applications_all, name='hr-view-applications-all'),
    url(r'application/add-comment/$', hrapplications.add_application_comment, name='hr-add-application-comment'),
    url(r'application/approve/(?P<application>\w+)/$', hrapplications.approve_application, name='hr-approve-application'),
    url(r'application/deny/(?P<application>\w+)/$', hrapplications.deny_application, name='hr-deny-application'),
    url(r'application/assign/(?P<application>\w+)/(?P<user>\w+)/$', hrapplications.assign_application, name='hr-assign-application')
    ]
