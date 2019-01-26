from django.conf.urls import include, url
from modules.eveonline.views import eve_online, sso

## BASE
urlpatterns = [
    url(r'^$', eve_online.dashboard, name='eve_online-dashboard'),
    url(r'^character/(?P<character>\w+)/$', eve_online.view_character, name='eve_online-view-character'),
    url(r'^character/set-main-character/(?P<character>\w+)/$', eve_online.set_main_character, name='eve_online-set-main-character'),
    url(r'^character/set-alt-character/(?P<character>\w+)/(?P<alt_type>\w+)/$', eve_online.set_alt_character, name='eve_online-set-alt-character')
    # url(r'^apply/$', eve_online.apply, name='eve_online-apply'),
]

## CHARACTERS
urlpatterns += [
    url(r'^characters/', eve_online.view_characters, name='eve_online-view-characters'),
]
# ## MODULES
# fleets
urlpatterns += [
    # url(r'^fleets/', fleet.view_fleets, name='view-fleets'),
    # url(r'^fleets/create/', fleet.create_fleet, name='create-fleet'),
    # url(r'^fleets/view/(?P<fleet_id>\d+)', fleet.view_fleet, name='view-fleet'),
    # url(r'^fleets/edit/(?P<fleet_id>\d+)', fleet.edit_fleet, name='edit-fleet'),
    # url(r'^fleets/delete/(?P<fleet_id>\d+)', fleet.delete_fleet, name='delete-fleet')
]

## SSO
urlpatterns += [
    url(r'^add-sso-token/$', sso.add_token, name='add-sso-token'),
    url(r'^remove-sso-token/(?P<character>\w+)/$', sso.remove_token, name='remove-sso-token'),
    url(r'^refresh-sso-token/(?P<character>\w+)/$', sso.refresh_token, name='refresh-sso-token'),
    url(r'^sso/callback/$', sso.receive_token, name='receive-sso-token'),
]
