from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from core.models import GroupEntity, GroupRequest
from core.decorators import login_required
from . import base

@login_required
def group_apply(request, group):
    group = Group.objects.get(pk=group)
    group_request = GroupRequest(user=request.user, status="Pending", group=group)
    group_request.save()
    return redirect('groups')

@login_required
def group_add_user(request, group, user):
    group = Group.objects.get(pk=group)
    user = User.objects.get(pk=user)
    group_request = GroupRequest.objects.get(user=user, status="Pending", group=group)
    group_request.status = "Accepted"
    user.groups.add(group)
    user.save()
    group_request.save()
    return redirect('groups')

@login_required
def group_remove_user(request, group, user):
    group = Group.objects.get(pk=group)
    user = User.objects.get(pk=user)
    group_request = GroupRequest.objects.get(user=user, status="Pending", group=group)
    group_request.status = "Vetoed"
    user.groups.remove(group)
    user.save()
    group_request.save()
    return redirect('groups')
