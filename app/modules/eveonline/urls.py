from django.conf.urls import include, url
from modules.eveonline.views import eve_online, sso

## BASE
urlpatterns = [
    url(r'^$', eve_online.dashboard, name='eve-dashboard'),
    url(r'^character/(?P<character>\w+)/$', eve_online.view_character, name='eve_online-view-character'),
    url(r'^character/set-main-character/(?P<character>\w+)/$', eve_online.set_main_character, name='eve_online-set-main-character'),
    url(r'^character/set-alt-character/(?P<character>\w+)/(?P<alt_type>\w+)/$', eve_online.set_alt_character, name='eve_online-set-alt-character'),
    url(r'^characters/', eve_online.view_characters, name='eve-online-characters'),
]

## CORPORATIONS
urlpatterns += [
    url(r'^corporations/audit/', eve_online.view_characters, name='eve-online-corporation-audit'),
    url(r'^corporations/taxes/', eve_online.view_characters, name='eve-online-corporation-taxes'),
]
## SSO
urlpatterns += [
    url(r'^add-sso-token/$', sso.add_token, name='add-sso-token'),
    url(r'^remove-sso-token/(?P<character>\w+)/$', sso.remove_token, name='remove-sso-token'),
    url(r'^refresh-sso-token/(?P<character>\w+)/$', sso.refresh_token, name='refresh-sso-token'),
    url(r'^sso/callback/$', sso.receive_token, name='receive-sso-token'),
]
