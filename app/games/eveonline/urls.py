from django.conf.urls import include, url
from games.eveonline.views import eve, sso

## BASE
urlpatterns = [
    url(r'^$', eve.dashboard, name='eve-dashboard'),
    url(r'^character/(?P<character>\w+)/$', eve.view_character, name='eve-view-character')
]

## SSO
urlpatterns += [
    url(r'^add-sso-token/$', sso.add_token, name='add-sso-token'),
    url(r'^remove-sso-token/$', sso.remove_token, name='remove-sso-token'),
    url(r'^sso/callback/$', sso.receive_token, name='receive-sso-token'),
]
