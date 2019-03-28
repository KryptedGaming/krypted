from django.conf.urls import url
from .views import applications

urlpatterns = [
    url(r'^$', applications.dashboard, name='view-applications'),
    url(r'^add/(?P<group_id>\w+)/$', applications.add_application, name='add-application'),
    url(r'^view/(?P<pk>\w+)/$', applications.view_application, name='view-application'),
    url(r'^application/approve/(?P<application>\w+)/$', applications.approve_application, name='approve-application'),
    url(r'^application/deny/(?P<application>\w+)/$', applications.deny_application, name='deny-application'),
    url(r'^application/assign/(?P<application>\w+)/(?P<user>\w+)/$', applications.assign_application, name='assign-application')
]
