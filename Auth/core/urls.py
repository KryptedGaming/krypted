from django.conf.urls import include, url
from django.contrib import admin
from . import views

## BASE
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
]

