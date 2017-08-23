from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='discord_index'),
    url(r'^callback$', views.callback, name='discord_callback'),
]
