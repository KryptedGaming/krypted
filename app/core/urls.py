from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import views, accounts, events, groups, applications

## BASE
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^guilds/$', views.guilds, name='guilds'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^members/$', views.view_members, name='view-members'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', accounts.login_user, name='login'),
    url(r'^logout/$', accounts.logout_user, name='logout'),
    url(r'^register/$', accounts.register_user, name='register'),
]

# GROUPS
urlpatterns += [
    url(r'^groups/apply/group=(?P<group>\d+)/$', groups.group_apply, name='group-apply'),
    url(r'^groups/adduser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_add_user, name='group-add-user'),
    url(r'^groups/removeuser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_remove_user, name='group-remove-user'),
]

## PASSWORD RESET
urlpatterns += [
    url(r'^password/reset$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

## EVENTS
## THESE WILL BE IMPLEMENTED ON A PROJECT LEVEL FOR NOW
# urlpatterns += [
#     url(r'^events/view/all/$', events.all_events, name='all-events'),
#     url(r'^events/view/(?P<pk>\d+)/$', events.view_event, name='view-event'),
#     url(r'^events/modify/(?P<pk>\d+)/$', events.modify_event, name='modify-event'),
#     url(r'^events/delete/(?P<pk>\d+)/$', events.delete_event, name='delete-event'),
#     url(r'^events/create/$', events.create_event, name='create-event'),
# ]


## APPLICATIONS
urlpatterns += [
    # overrides
    url(r'^applications/add/eve/$', applications.add_eve_application, name='hr-add-eve-application'),
    # base
    url(r'^applications/$', views.applications, name='hr-view-applications'),
    url(r'^applications/add/(?P<slug>\w+)/$', applications.add_application, name='hr-add-application'),
    url(r'^applications/view/(?P<pk>\w+)/$', applications.view_application, name='hr-view-application'),
    url(r'^applications/application/approve/(?P<application>\w+)/$', applications.approve_application, name='hr-approve-application'),
    url(r'^applications/application/deny/(?P<application>\w+)/$', applications.deny_application, name='hr-deny-application'),
    url(r'^applications/application/assign/(?P<application>\w+)/(?P<user>\w+)/$', applications.assign_application, name='hr-assign-application')
]
