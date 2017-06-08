from django.conf.urls import include, url
from django.contrib import admin
from . import views

## BASE
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
]

## PROFILES
urlpatterns += [
    url(r'^profile/view/all/$', views.all_profiles, name='all_profiles'),
    url(r'^profile/view/(?P<pk>\d+)/$', views.view_profile, name='view-profile'),
    url(r'^profile/create/$', views.create_profile, name='create-profile'),
    url(r'^profile/delete/(?P<pk>\d+)/$', views.delete_profile, name='delete-profile'),
    url(r'^profile/modify/(?P<pk>\d+)/$', views.modify_profile, name='modify-profile'),
    # HELPERS
    url(r'^profile/(?P<pk>\d+)/add-game/name=(?P<game>\d+)/$',views.profile_add_game, name='profile-add-game'),
    url(r'^profile/(?P<pk>\d+)/remove-game/name=(?P<game>\d+)/$', views.profile_remove_game, name='profile-remove-game'),
]

## NOTIFICATIONS
urlpatterns += [
    url(r'^notifications/user/(?P<username>\w+)/$', views.all_notifications, name='all-notifications'),
    url(r'^notification/view/(?P<pk>\d+)/$', views.view_notification, name='view-notification'),
    url(r'^notification/create/$', views.create_notification, name='create-notification'),
    url(r'^notification/delete/(?P<pk>\d+)/$', views.delete_notification, name='delete-notification'),
    url(r'^notification/modify/(?P<pk>\d+)/$', views.modify_notification, name='modify-notification'),
]

## GAMES
urlpatterns += [
    url(r'^games/all/$', views.all_games, name='all-games'),
    url(r'^game/view/(?P<pk>\d+)/$', views.view_game, name='view-game'),
    url(r'^game/create/', views.create_game, name='create-game'),
    url(r'^game/delete/(?P<pk>\d+)/$', views.delete_game, name='delete-game'),
    url(r'^game/modify/(?P<pk>\d+)/$', views.modify_game, name='modify-game'),
]

# MISC
urlpatterns += [
    url(r'^no-permissions/$', views.no_permissions, name='no_permissions'),
]
