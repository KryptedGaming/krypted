from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from core.models import GroupEntity, GroupRequest
from core.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import base
import logging

logger = logging.getLogger(__name__)

@login_required
def hard_sync(request):
    logger.info("%s has requested a hard sync." % request.user)
    groups = request.user.groups.all()
    for group in groups:
        request.user.groups.remove(group)
    for group in groups:
        request.user.groups.add(group)
    messages.add_message(request, messages.SUCCESS, 'Your groups have been synced.')
    return redirect('dashboard')

@login_required
def group_apply(request, group):
    group = GroupEntity.objects.get(group__pk=group)
    group_request = GroupRequest(user=request.user, status="Pending", group=group)
    if group.public:
        group_request.status = "Accepted"
        request.user.groups.add(group.group)
        request.user.save()
    group_request.save()
    return redirect('groups')

@login_required
@permission_required('manage_group_requests')
def group_add_user(request, group, user):
    group = Group.objects.get(pk=group)
    user = User.objects.get(pk=user)
    group_request = GroupRequest.objects.get(user=user, status="Pending", group=GroupEntity.objects.get(group=group))
    group_request.status = "Accepted"
    user.groups.add(group)
    user.save()
    group_request.save()
    return redirect('groups')

@login_required
def group_remove_user(request, group, user):
    group = Group.objects.get(pk=group)
    user = User.objects.get(pk=user)
    logger.info("Group_remove_user called")
    if request.user.has_perm('manage_group_requests') or user is request.user:
        group_request = GroupRequest.objects.get(user=user, group=GroupEntity.objects.get(group=group))
        user.groups.remove(group)
        user.save()
        group_request.delete()
    else:
        logger.info("User %s does not have permission for that." % request.user.username)
    return redirect('groups')
