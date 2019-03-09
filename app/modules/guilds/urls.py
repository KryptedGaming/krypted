from django.conf.urls import url
from .views import guilds, applications

urlpatterns = []

# GUILDS
urlpatterns += [
    url(r'^$', guilds.dashboard, name='guilds'),
    url(r'^users/$', guilds.user_list, name='guild-users'),
    url(r'^users/remove/(?P<guild_id>\w+)/(?P<user_id>\w+)', guilds.remove_guild_user, name='remove-guild-user')
]

## APPLICATIONS
urlpatterns += [
    # base
    url(r'^applications/$', applications.dashboard, name='hr-view-applications'),
    url(r'^applications/add/(?P<slug>\w+)/$', applications.add_application, name='hr-add-application'),
    url(r'^applications/view/(?P<pk>\w+)/$', applications.view_application, name='hr-view-application'),
    url(r'^applications/application/approve/(?P<application>\w+)/$', applications.approve_application, name='hr-approve-application'),
    url(r'^applications/application/deny/(?P<application>\w+)/$', applications.deny_application, name='hr-deny-application'),
    url(r'^applications/application/assign/(?P<application>\w+)/(?P<user>\w+)/$', applications.assign_application, name='hr-assign-application')
]
