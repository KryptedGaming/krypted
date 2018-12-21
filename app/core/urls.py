from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import views, accounts, events, groups, applications, guilds
from core.views.events import EventUpdate

## BASE
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', accounts.login_user, name='login'),
    url(r'^logout/$', accounts.logout_user, name='logout'),
    url(r'^register/$', accounts.register_user, name='register'),
    url(r'^verify/confirmation/(?P<token>[0-9A-Za-z_\-]+)/$', accounts.verify_confirm, name='verify-confirm'),
    url(r'^user/(?P<pk>\d+)/$', accounts.edit_user, name='edit_user')
]

# GUILDS
urlpatterns += [
    url(r'^guilds/$', guilds.dashboard, name='guilds'),
]

# GROUPS
urlpatterns += [
    url(r'^groups/$', groups.dashboard, name='groups'),
    url(r'^groups/apply/group=(?P<group>\d+)/$', groups.group_apply, name='group-apply'),
    url(r'^groups/adduser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_add_user, name='group-add-user'),
    url(r'^groups/removeuser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_remove_user, name='group-remove-user'),
]

## PASSWORD RESET
urlpatterns += [
    url(r'^password/reset$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

## EVENTS
from core.feeds import EventFeed
urlpatterns += [
    url(r'^events/view/all/$', events.dashboard, name='all-events'),
    url(r'^events/view/(?P<pk>\d+)/$', events.view_event, name='view-event'),
    url(r'^events/create/$', events.add_event, name='add-event'),
    url(r'^events/modify/(?P<pk>\d+)/$', events.edit_event, name='edit-event'),
    url(r'^events/delete/(?P<pk>\d+)/$', events.remove_event, name='remove-event'),
    url(r'^latest/feed.ics$', EventFeed())
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
