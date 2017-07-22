from django.shortcuts import render

# Create your views here.
## BASE
urlpatterns = [
    url(r'^$', base.dashboard, name='dashboard'),
    url(r'^guilds/$', base.guilds, name='guilds'),
    url(r'^games/$', base.games, name='games'),
    url(r'^profile/$', base.profile, name='profile'),
    url(r'^notifications/$', base.notifications, name='notifications'),
]
