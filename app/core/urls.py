from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import base, user, profile, events, groups

## BASE
urlpatterns = [
    url(r'^$', base.dashboard, name='dashboard'),
    url(r'^guilds/$', base.guilds, name='guilds'),
    # url(r'^groups/$', base.groups, name='groups'),
    # url(r'^games/$', base.games, name='games'),
    # url(r'^games/(?P<tab>\w+)/$', base.games, name='games'),
    # url(r'^profile/$', base.profile, name='profile'),
    # url(r'^notifications/$', base.notifications, name='notifications'),
    # url(r'^members/$', base.view_members, name='view-members'),
]

## USER AUTHENTICATION
urlpatterns += [
    # url(r'^login/$', user.login_user, name='login'),
    # url(r'^logout/$', user.logout_user, name='logout'),
    # url(r'^register/$', user.register_user, name='register'),
]

## PROFILES
# urlpatterns += [
#     url(r'^profile/create/$', profile.create_profile, name='create-profile'),
#     # HELPERS
#     url(r'^profile/add-game/name=(?P<game_to_add>\d+)/$',
#         profile.profile_add_game, name='profile-add-game'),
#     url(r'^profile/remove-game/name=(?P<game_to_remove>\d+)/$',
#         profile.profile_remove_game, name='profile-remove-game'),
#     url(r'^profile/add-guild/name=(?P<guild>\d+)/$',
#         profile.profile_add_guild, name='profile-add-guild'),
#     url(r'^profile/remove-guild/name=(?P<guild>\d+)/$',
#         profile.profile_remove_guild, name='profile-remove-guild'),
# ]

## GROUPS
# urlpatterns += [
#     url(r'^groups/apply/group=(?P<group>\d+)/$', groups.group_apply, name='group-apply'),
#     url(r'^groups/adduser/group=(?P<group>\d+)/user=(?P<user>\d+)/$', groups.group_add_user, name='group-add-user'),
#     url(r'^groups/removeuser/group=(?P<group>\d+)/user=(?P<user>\d+)/$', groups.group_remove_user, name='group-remove-user'),
#     url(r'^groups/hard-sync/', groups.hard_sync, name='group-hard_sync')
# ]

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
