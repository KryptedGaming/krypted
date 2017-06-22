from django.conf.urls import include, url
from eveonline.views import eve
## BASE
urlpatterns = [
    url(r'^$', eve.dashboard, name='eve-dashboard'),
]
