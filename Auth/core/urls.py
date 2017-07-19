from django.conf.urls import include, url
from django.contrib import admin
from core.views import base, user, profile, events, notifications

## BASE
urlpatterns = [
    url(r'^$', base.dashboard, name='dashboard'),
    url(r'^guilds/$', base.guilds, name='guilds'),
    url(r'^games/$', base.games, name='games'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', user.login_user, name='login'),
    url(r'^logout/$', user.logout_user, name='logout'),
    url(r'^register/$', user.register_user, name='register'),
]

## PROFILES
urlpatterns += [
    url(r'^profile/$', profile.profile, name='profile'),
    url(r'^profile/create/$', profile.create_profile, name='create-profile'),
    url(r'^profile/delete/(?P<pk>\d+)/$', profile.delete_profile, name='delete-profile'),
    # HELPERS
    url(r'^profile/add-game/name=(?P<game_to_add>\d+)/$',
        profile.profile_add_game, name='profile-add-game'),
    url(r'^profile/remove-game/name=(?P<game>\d+)/$',
        profile.profile_remove_game, name='profile-remove-game'),
    url(r'^profile/add-guild/name=(?P<guild>\d+)/$',
        profile.profile_add_guild, name='profile-add-guild'),
    url(r'^profile/remove-guild/name=(?P<guild>\d+)/$',
        profile.profile_remove_guild, name='profile-remove-guild'),
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

## NOTIFICATIONS
urlpatterns += [
    url(r'^notifications/$', notifications.notifications, name='notifications'),
]

# MISC
urlpatterns += [
    url(r'^no-permissions/$', base.no_permissions, name='no_permissions'),
]
