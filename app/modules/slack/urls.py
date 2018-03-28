from modules.slack import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^resend/$', views.resend, name='slack_resend'),
    url(r'^add-slack-channel/$', views.add_slack_channel, name='slack_add_channel'),
]
