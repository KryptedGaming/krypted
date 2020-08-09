from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(),
         name="accounts-register"),
    path('login/', views.UserLogin.as_view(), name="accounts-login"),
    path('logout/', views.UserLogout.as_view(), name="accounts-logout"),
    path('password/reset/', auth_views.PasswordResetView.as_view(),
         name='accounts-password-reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    re_path(r'^activate/(?P<token>[0-9A-Za-z_\-]+)/$',
            views.activate_account, name='accounts-activate'),
    re_path(r'^user/(?P<username>[0-9A-Za-z_\-\.]+)/$',
            views.UserView.as_view(), name='accounts-user'),
    path('user/delete/<int:pk>/', views.UserDelete.as_view(),
         name='accounts-user-delete'),

]
