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
    # overrides
    url(r'^add/eve/$', hrapplications.add_eve_application, name='hr-add-eve-application'),
    # base
    url(r'^add/(?P<slug>\w+)/$', hrapplications.add_application, name='hr-add-application'),
    url(r'^change/(?P<id>\d+)/$', hrapplications.change_application, name='hr-change-application'),
    url(r'^delete/(?P<id>\d+)/$', hrapplications.delete_application, name='hr-delete-application'),
    url(r'^view/(?P<pk>\w+)/$', hrapplications.view_application, name='hr-view-application'),
    url(r'^view/$', hrapplications.view_applications_all, name='hr-view-applications-all'),
    url(r'application/add-comment/$', hrapplications.add_application_comment, name='hr-add-application-comment'),
    url(r'application/approve/(?P<application>\w+)/$', hrapplications.approve_application, name='hr-approve-application'),
    url(r'application/deny/(?P<application>\w+)/$', hrapplications.deny_application, name='hr-deny-application'),
    url(r'application/assign/(?P<application>\w+)/(?P<user>\w+)/$', hrapplications.assign_application, name='hr-assign-application')
    ]
