from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import views, accounts, groups

## BASE
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]

## USER AUTHENTICATION
urlpatterns += [
    url(r'^login/$', accounts.login_user, name='login'),
    url(r'^logout/$', accounts.logout_user, name='logout'),
    url(r'^register/$', accounts.register_user, name='register'),
    url(r'^verify/confirmation/(?P<token>[0-9A-Za-z_\-]+)/$', accounts.verify_confirm, name='verify-confirm'),
    url(r'^user/(?P<pk>\d+)/$', accounts.edit_user, name='edit_user')
]

# GROUPS
urlpatterns += [
    url(r'^groups/$', groups.dashboard, name='groups'),
    url(r'^groups/apply/group=(?P<group>\d+)/$', groups.group_apply, name='group-apply'),
    url(r'^groups/adduser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_add_user, name='group-add-user'),
    url(r'^groups/removeuser/group=(?P<group_id>\d+)/user=(?P<user_id>\d+)/$', groups.group_remove_user, name='group-remove-user'),
]

## PASSWORD RESET
urlpatterns += [
    url(r'^password/reset$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

