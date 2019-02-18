# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.apps import apps
# LOCAL IMPORTS
from core.models import GroupRequest
from core.decorators import services_required
# EXTERNAL IMPORTS
# from modules.discord.tasks import send_discord_message
# MISC
import logging

logger = logging.getLogger(__name__)

@login_required
@services_required
def dashboard(request, **kwargs):
    context = {}
    groups = []
    # PERMISSIONS
    context['manage'] = request.user.has_perm('change_grouprequest')
    context['audit'] = request.user.has_perm('change_grouprequest')

    if apps.is_installed("modules.guilds"):
        for group in Group.objects.filter(guilds=None):
            if group.info.type == "PUBLIC":
                groups.append({
                    'group': group,
                    'requested': request.user.info.has_group_request(group)
                })
            elif group.info.type == "PROTECTED":
                groups.append({
                    'group': group,
                    'user_has_group': (group in request.user.groups.all()),
                    'requested': request.user.info.has_group_request(group)
                })

        for guild in request.user.guilds_in.all():
            for group in guild.groups.all():
                if group.info.type == "PUBLIC":
                    groups.append({
                        'group': group,
                        'requested': request.user.info.has_group_request(group)
                    })
                elif group.info.type == "PROTECTED":
                    groups.append({
                        'group': group,
                        'user_has_group': (group in request.user.groups.all()),
                        'requested': request.user.info.has_group_request(group)
                    })
    else:
        for group in Group.objects.all():
            if group.info.type == "PUBLIC":
                groups.append({
                    'group': group,
                    'requested': request.user.info.has_group_request(group)
                })
            elif group.info.type == "PROTECTED":
                groups.append({
                    'group': group,
                    'user_has_group': (group in request.user.groups.all()),
                    'requested': request.user.info.has_group_request(group)
                })

    context['groups'] = groups

    # PENDING VIEW
    if context['manage']:
        group_requests = []
        for group_request in GroupRequest.objects.filter(response_action="Pending"):
            if not group_request.request_group.info.managers.all() or request.user in group_request.request_group.info.managers.all():
                permission = True
            else:
                permission = False
            group_requests.append({
                'request': group_request,
                'permission': permission
                })
        context['group_requests'] = group_requests

    # AUDIT VIEW
    if context['audit']:
        group_requests = []
        for group_request in GroupRequest.objects.filter(response_action="Accepted"):
            group_requests.append({
                'request': group_request,
                'permission': True
                })
        context['audit_requests'] = group_requests

    return render(request, 'core/groups.html', context)

@login_required
@services_required
def group_apply(request, group):
    group = Group.objects.get(id=group)
    group_request = GroupRequest(request_user=request.user, response_action="Pending", request_group=group)

    # Is this user allowed to apply? 
    # - If guilds is enabled verify that the group and user are both part of a common guild OR the group is not part of a guild.
    # - If guilds is not enabled then any PUBLIC or PROTECTED group is fair game
    allowed = False
    if group.info.type in ['PUBLIC','PROTECTED']:
        if apps.is_installed("modules.guilds"):
            group_guilds = group.guilds.all()
            if not group_guilds or (request.user.guilds_in.all() & group_guilds):
                allowed = True
        else:
            allowed = True

    if allowed:
        if group.info.type == "PUBLIC":
            group_request.response_action = "Accepted"
            request.user.groups.add(group)
            request.user.save()
        group_request.save()
        # notify_discord_channel(group_request, group_request.request_group.guild)
    else:
        messages.add_message(request, messages.ERROR, "You are not allowed to apply to group '%s'." % group.name)

    return redirect('groups')

@login_required
@permission_required('change_grouprequests')
def group_add_user(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group_request = GroupRequest.objects.get(request_user=user, response_action="Pending", request_group=Group.objects.get(id=group_id))
    group_request.response_action = "Accepted"
    user.groups.add(group_request.request_group)
    user.save()
    group_request.save()
    # notify_user(group_request, "APPROVED")
    return redirect('groups')

@login_required
def group_remove_user(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    if request.user.has_perm('delete_grouprequests') or request.user == user:
        user.groups.remove(Group.objects.get(pk=group_id))
        user.save()
        try:
            group_request = GroupRequest.objects.filter(request_user=user, request_group=Group.objects.get(id=group_id)).first()
            group_request.delete()
        except Exception as e:
            logger.error(e)
        # notify_user(group_request, "REMOVED")
    return redirect('groups')

# HELPERS
# def notify_discord_channel(group_request, guild):
#     if guild and guild.slug in discord_settings.GUILD_ADMIN_CHANNELS:
#         channel = discord_settings.GUILD_ADMIN_CHANNELS[guild.slug]
#         send_discord_message(
#         channel,
#         "%s (%s) has applied to %s. https://auth.kryptedgaming.com/groups/" % (group_request.request_user.discord, group_request.request_user, group_request.request_group)
#         )
#
# def notify_user(group_request, type):
#     try:
#         channel = "#bot"
#         send_discord_message(
#         channel,
#         "Your group request to %s has been %s." % (group_request.request_group, type),
#         user=group_request.request_user.id
#         )
#     except KeyError:
#         logger.warning("Please define a #bot channel to notify users of group updates.")
#     except Exception as e:
#         logger.warning(e)
