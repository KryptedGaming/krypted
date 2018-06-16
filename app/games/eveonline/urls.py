from django.conf.urls import include, url
from games.eveonline.views import eve, sso
from games.eveonline.modules.fleet import views as fleet

## BASE
urlpatterns = [
    url(r'^$', eve.dashboard, name='eve-dashboard'),
    url(r'^character/(?P<character>\w+)/$', eve.view_character, name='eve-view-character'),
    url(r'^character/set-main-character/(?P<character>\w+)/$', eve.set_main_character, name='eve-set-main-character'),
    url(r'^character/set-alt-character/(?P<character>\w+)/(?P<alt_type>\w+)/$', eve.set_alt_character, name='eve-set-alt-character')
    # url(r'^apply/$', eve.apply, name='eve-apply'),
]

# ## MODULES
# fleets
urlpatterns += [
    url(r'^fleets/', fleet.view_fleets, name='view-fleets'),
    url(r'^fleets/create/', fleet.create_fleet, name='create-fleet'),
    url(r'^fleets/view/(?P<fleet_id>\d+)', fleet.view_fleet, name='view-fleet'),
    url(r'^fleets/edit/(?P<fleet_id>\d+)', fleet.edit_fleet, name='edit-fleet'),
    url(r'^fleets/delete/(?P<fleet_id>\d+)', fleet.delete_fleet, name='delete-fleet')
]

## SSO
urlpatterns += [
    url(r'^add-sso-token/$', sso.add_token, name='add-sso-token'),
    url(r'^remove-sso-token/(?P<character>\w+)/$', sso.remove_token, name='remove-sso-token'),
    url(r'^refresh-sso-token/(?P<character>\w+)/$', sso.refresh_token, name='refresh-sso-token'),
    url(r'^sso/callback/$', sso.receive_token, name='receive-sso-token'),
]
