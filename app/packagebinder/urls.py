from django.urls import path
from . import views 

urlpatterns = [
    path('', views.setup, name="app-setup"),
    path('package/<str:package_name>/settings/update', views.update_package_settings, name="app-update-package-settings"),
    path('api/tasks/enable', views.enable_task, name="app-enable-task"),
    path('api/tasks/disable', views.disable_task, name="app-disable-task"),
]
