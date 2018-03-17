from modules.slack import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^resend/$', views.resend, name='slack_resend'),
]
