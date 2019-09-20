"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.apps import apps
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.defaults import server_error
from . import views

import logging
logger = logging.getLogger(__name__)

urlpatterns = [
    path('', views.dashboard, name="app-dashboard"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('500/', server_error)
]

for application in settings.INSTALLED_APPS:
    try:
        app_config = apps.get_app_config(application)
        try:
            if app_config.url_slug:
                urlpatterns += [
                    path('%s/' % app_config.url_slug, include('%s.urls' % application))
                ]
        except AttributeError as exception:
            print("Skipping %s: %s" % (application, exception))
    except LookupError as exception:
        print("Skipping %s: %s" % (application, exception))
    
handler500 = views.handler500

# DEVELOPMENT
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
