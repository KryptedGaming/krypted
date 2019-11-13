from django.urls import path
from . import views 

urlpatterns = [
    path('', views.view_applications, name='application-list'),
    path('my/', views.view_my_applications, name='my-applications'),
    path('<int:application_id>/approve/', views.approve_application, name='application-approve'),
    path('deny/application/<int:application_id>/', views.deny_application, name='application-deny'),
    path('<int:pk>/', views.view_application, name='application-detail'),
    path('template/<int:template_id>/new/', views.create_application, name='application-create'),
    path('<int:application_id>/assign/', views.assign_application_to_user, name='application-assign'),
]