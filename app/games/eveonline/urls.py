from django.conf.urls import include, url
from games.eveonline.views import eve, sso

## BASE
urlpatterns = [
    url(r'^$', eve.dashboard, name='eve-dashboard'),
    url(r'^apply/$', eve.apply, name='eve-apply'),
    url(r'^character/(?P<character>\w+)/$', eve.view_character, name='eve-view-character'),
    url(r'^character/set-main-character/(?P<character>\w+)/$', eve.set_main_character, name='eve-set-main-character'),
    url(r'^character/set-alt-character/(?P<character>\w+)/(?P<alt_type>\w+)/$', eve.set_alt_character, name='eve-set-alt-character')
    # url(r'^apply/$', eve.apply, name='eve-apply'),
]

# ## MODULES
# urlpatterns = [
#     url(r'^audit/', include('games.eveonline.modules.audit.urls')),
# ]

## SSO
urlpatterns += [
    url(r'^add-sso-token/$', sso.add_token, name='add-sso-token'),
    url(r'^remove-sso-token/(?P<character>\w+)/$', sso.remove_token, name='remove-sso-token'),
    url(r'^refresh-sso-token/(?P<character>\w+)/$', sso.refresh_token, name='refresh-sso-token'),
    url(r'^sso/callback/$', sso.receive_token, name='receive-sso-token'),
]
