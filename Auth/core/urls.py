from django.conf.urls import include, url
from django.contrib import admin
from core.views import base, user, profile, events, notifications

## BASE
urlpatterns = [
    url(r'^$', base.dashboard, name='dashboard'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', user.login_user, name='login'),
    url(r'^logout/$', user.logout_user, name='logout'),
    url(r'^register/$', user.register_user, name='register'),
]

## PROFILES
urlpatterns += [
    url(r'^profile/view/all/$', profile.all_profiles, name='all_profiles'),
    url(r'^profile/view/(?P<pk>\d+)/$', profile.view_profile, name='view-profile'),
    url(r'^profile/create/$', profile.create_profile, name='create-profile'),
    url(r'^profile/delete/(?P<pk>\d+)/$', profile.delete_profile, name='delete-profile'),
    url(r'^profile/modify/(?P<pk>\d+)/$', profile.modify_profile, name='modify-profile'),
    # HELPERS
    url(r'^profile/(?P<pk>\d+)/add-game/name=(?P<game>\d+)/$',
        profile.profile_add_game, name='profile-add-game'),
    url(r'^profile/(?P<pk>\d+)/remove-game/name=(?P<game>\d+)/$',
        profile.profile_remove_game, name='profile-remove-game'),
]

## EVENTS 
urlpatterns += [
    url(r'^events/view/all/$', events.all_events, name='all-events'),
    url(r'^events/view/(?P<pk>\d+)/$', events.view_event, name='view-event'),
    url(r'^events/modify/(?P<pk>\d+)/$', events.modify_event, name='modify-event'),
    #url(r'^events/delete/(?P<pk>\d+)/$', views.delete_event, name='delete-event'),
    url(r'^events/create/$', events.create_event, name='create-event'),
]

## NOTIFICATIONS
urlpatterns += [
    url(r'^notifications/user/(?P<username>\w+)/$', notifications.all_notifications, name='all-notifications'),
    url(r'^notification/view/(?P<pk>\d+)/$', notifications.view_notification, name='view-notification'),
    url(r'^notification/create/$', notifications.create_notification, name='create-notification'),
    url(r'^notification/delete/(?P<pk>\d+)/$', notifications.delete_notification, name='delete-notification'),
    url(r'^notification/modify/(?P<pk>\d+)/$', notifications.modify_notification, name='modify-notification'),
]

### GAMES
#urlpatterns += [
#    url(r'^games/all/$', views.all_games, name='all-games'),
#    url(r'^game/view/(?P<pk>\d+)/$', views.view_game, name='view-game'),
#    url(r'^game/create/', views.create_game, name='create-game'),
#    url(r'^game/delete/(?P<pk>\d+)/$', views.delete_game, name='delete-game'),
#    url(r'^game/modify/(?P<pk>\d+)/$', views.modify_game, name='modify-game'),
#]

# MISC
urlpatterns += [
    url(r'^no-permissions/$', base.no_permissions, name='no_permissions'),
]
