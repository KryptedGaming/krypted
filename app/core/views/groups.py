from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from core.models import User, Group, GroupRequest
from core.decorators import login_required, permission_required, services_required
import logging

logger = logging.getLogger(__name__)
@login_required
@services_required
def group_apply(request, group):
    group = Group.objects.get(id=group)
    group_request = GroupRequest(request_user=request.user, response_action="Pending", request_group=group)
    if group.type == "PUBLIC":
        group_request.response_action = "Accepted"
        request.user.groups.add(group.group)
        request.user.save()
    group_request.save()
    return redirect('groups')

@login_required
@permission_required('core.manage_group_requests')
def group_add_user(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group_request = GroupRequest.objects.get(request_user=user, response_action="Pending", request_group=Group.objects.get(id=group_id))
    group_request.response_action = "Accepted"
    user.groups.add(group_request.request_group)
    user.save()
    group_request.save()
    return redirect('groups')

@login_required
@permission_required('core.manage_group_requests')
def group_remove_user(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group_request = GroupRequest.objects.filter(request_user=user, request_group=Group.objects.get(id=group_id)).first()
    user.groups.remove(group_request.request_group)
    user.save()
    group_request.delete()
    return redirect('groups')
