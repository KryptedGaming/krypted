from django.conf.urls import include, url, handler500
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.apps import apps
from core.views import base as error_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),
    url(r'^eve/', include('games.eveonline.urls')),
    url(r'^applications/', include('modules.hrapplications.urls')),
    url(r'^discord/', include('modules.discord.urls')),
    url(r'^discourse/', include('modules.discourse.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')), name='favicon')
]

# CONDITIONAL MODULES
if apps.is_installed('modules.slack'):
    urlpatterns += [
    url(r'^slack/', include('modules.slack.urls')),
    ]
