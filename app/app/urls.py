from django.conf.urls import include, url, handler500
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import permission_required, login_required
from django.apps import apps
# EXTERNAL IMPORTS
from core.decorators import services_required
# MISC
from decorator_include import decorator_include

# CORE
urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')), name='favicon')
]

# MODULES
if apps.is_installed("modules.guilds"):
    urlpatterns += [
        url(r'^guilds/', decorator_include(services_required, 'modules.guilds.urls')),
    ]
if apps.is_installed("modules.applications"):
    urlpatterns += [
        url(r'^applications/', decorator_include(services_required, 'modules.applications.urls')),
    ]
if apps.is_installed("modules.discord"):
    urlpatterns += [
        url(r'^discord/', include('modules.discord.urls')),
    ]
if apps.is_installed("modules.discourse"):
    urlpatterns += [
        url(r'^discourse/', include('modules.discourse.urls')),
    ]
if apps.is_installed("modules.eveonline"):
    urlpatterns += [
        url(r'^eve/', decorator_include(services_required, 'modules.eveonline.urls')),
    ]

if apps.is_installed("modules.engagement"):
    urlpatterns += [
        url(r'^engagement/', include('modules.engagement.urls')),
    ]

# DEVELOPMENT
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
