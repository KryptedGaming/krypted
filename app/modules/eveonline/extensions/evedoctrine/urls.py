from django.conf.urls import include, url
from modules.eveonline.extensions.evedoctrine import views

urlpatterns = [
    url(r'^$', views.doctrines, name='eve-online-doctrines'),
    url(r'^view/(?P<doctrine>\w+)/$', views.view_doctrine, name='eve-online-view-doctrine'),
    url(r'^fittings/$', views.fittings, name='eve-online-fittings'),
    url(r'^fittings/view/(?P<fitting>\w+)/$', views.view_fitting, name='eve-online-view-fitting'),
]