from django.conf.urls import include, url, handler500
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.apps import apps

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),
    url(r'^discord/', include('modules.discord.urls')),
    url(r'^discourse/', include('modules.discourse.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')), name='favicon')
]

# GAMES
urlpatterns += [
    url(r'^eve/', include('games.eveonline.urls')),
    # url(r'^rust/', RedirectView.as_view(url='/applications/add/rust/')),
    # url(r'^dnd/', RedirectView.as_view(url='/applications/add/dnd/')),
    # url(r'^wow/', RedirectView.as_view(url='/applications/add/wow/'))
]
