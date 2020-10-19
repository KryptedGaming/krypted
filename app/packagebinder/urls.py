from django.urls import path
from . import views 

urlpatterns = [
    path('', views.setup, name="app-setup"),
    path('api/tasks/enable', views.enable_task, name="app-enable-task"),
    path('api/tasks/disable', views.disable_task, name="app-disable-task"),
]
