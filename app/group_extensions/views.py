from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib.auth.models import Group
from .models import GroupRequest, ExtendedGroup
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
import datetime


@login_required
def view_groups(request):
    valid_extented_groups = get_valid_groups(request)

    groups = []
    for extended_group in valid_extented_groups:
        group = extended_group.group
        groups.append({
            "group": extended_group.group,
            "type": extended_group.type,
            "requested": GroupRequest.objects.filter(request_user=request.user, request_group=group, response_action="PENDING").first(),
            "request_count": GroupRequest.objects.filter(request_group=group, response_action="PENDING").count()
        })

    return render(request, 'group_extensions/view_groups.html', context={
        "groups": groups,
    })


@login_required
def request_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    valid_groups = [ext_group.group for ext_group in get_valid_groups(request)]
    if group not in valid_groups:
        messages.add_message(request, messages.WARNING,
                             'You do not have access to request that group.')
        return redirect('group-list')

    if ExtendedGroup.objects.filter(group=group, type="OPEN").exists():
        GroupRequest(
            request_user=request.user,
            request_group=group,
            response_action="ACCEPTED",
        ).save()

        request.user.groups.add(group)
        messages.add_message(request, messages.SUCCESS,
                             'Successfully joined %s' % group)
    else:
        GroupRequest(
            request_user=request.user,
            request_group=group,
        ).save()

        messages.add_message(request, messages.SUCCESS,
                             'Successfully requested %s' % group)
    return redirect('group-list')


@login_required
@permission_required('group_extensions.view_grouprequest', raise_exception=True)
def view_group_requests(request, group_id):
    group = Group.objects.get(pk=group_id)
    if request.user.has_perm('group_extensions.bypass_group_requirement') or group in request.user.groups.all():
        return render(request, 'group_extensions/view_group_requests.html', context={
            "group_requests": GroupRequest.objects.filter(request_group__pk=group_id, response_action="PENDING"),
            "group": group
        })
    else:
        messages.add_message(
            request, messages.ERROR, "You must be a member of that Group to view Group Requests, or must have bypass permission.")
        return redirect('group-list')


@login_required
@permission_required('group_extensions.change_grouprequest', raise_exception=True)
def approve_group_request(request, group_id, group_request_id):
    group = Group.objects.get(pk=group_id)
    group_request = GroupRequest.objects.get(pk=group_request_id)
    if request.user.has_perm('group_extensions.bypass_group_requirement') or group in request.user.groups.all():
        group_request.response_action = "ACCEPTED"
        group_request.response_user = request.user
        group_request.response_date = datetime.datetime.utcnow()
        group_request.save()
        group_request.request_user.groups.add(group)
        messages.add_message(request, messages.SUCCESS,
                             "Accepted Group Request.")
    else:
        messages.add_message(
            request, messages.ERROR, "You must be a member of that Group to accept Group Requests, or must have bypass permission.")
    return redirect('group-request-list', group_id)


@login_required
@permission_required('group_extensions.change_grouprequest', raise_exception=True)
def deny_group_request(request, group_id, group_request_id):
    group = Group.objects.get(pk=group_id)
    group_request = GroupRequest.objects.get(pk=group_request_id)
    if request.user.has_perm('group_extensions.bypass_group_requirement') or group in request.user.groups.all():
        group_request.response_action = "REJECTED"
        group_request.response_user = request.user
        group_request.response_date = datetime.datetime.utcnow()
        group_request.save()
        group_request.request_user.groups.remove(group)
        messages.add_message(request, messages.SUCCESS,
                             "Rejected Group Request.")
    else:
        messages.add_message(
            request, messages.ERROR, "You must be a member of that Group to reject Group Requests, or must have bypass permission.")
    return redirect('group-request-list', group_id)


# helper methods
def get_valid_groups(request):
    if request.user.has_perm('group_request.bypass_group_requirement'):
        return ExtendedGroup.objects.all()
    else:
        return (ExtendedGroup.objects.filter(enabling_groups__in=request.user.groups.all()) |
                ExtendedGroup.objects.filter(enabling_groups=None))
