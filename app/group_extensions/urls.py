from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.view_groups, name='group-list'),
    path('<int:group_id>/request/', views.request_group, name='group-request'),
    path('<int:group_id>/requests/', views.view_group_requests, name='group-request-list'),
    path('<int:group_id>/requests/<int:group_request_id>/approve/', views.approve_group_request, name='group-request-approve'),
    path('<int:group_id>/requests/<int:group_request_id>/deny/', views.deny_group_request, name='group-request-deny'),
]