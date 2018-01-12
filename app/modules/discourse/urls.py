from modules.discourse import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='discouse_index'),
    url(r'^sso$', views.sso, name='discouse_sso'),
]
