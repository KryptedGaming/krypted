from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from core.models import User, Group, GroupRequest
from core.decorators import login_required, permission_required, services_required, staff_required
from app.conf import discord as discord_settings
from modules.discord.tasks import send_discord_message
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
    if not group_request.request_group.type == "PUBLIC":
        notify_discord_channel(group_request, group_request.request_group.guild)
    return redirect('groups')

@login_required
@staff_required
def group_add_user(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group_request = GroupRequest.objects.get(request_user=user, response_action="Pending", request_group=Group.objects.get(id=group_id))
    group_request.response_action = "Accepted"
    user.groups.add(group_request.request_group)
    user.save()
    group_request.save()
    notify_user(group_request, "APPROVED")
    return redirect('groups')

@login_required
def group_remove_user(request, group_id, user_id):
    if request.user.has_perm('core.delete_group_request') or request.user.id == user_id:
        user = User.objects.get(id=user_id)
        user.groups.remove(Group.objects.get(pk=group_id))
        user.save()
        try:
            group_request = GroupRequest.objects.filter(request_user=user, request_group=Group.objects.get(id=group_id)).first()
            group_request.delete()
        except Exception as e:
            logger.error(e)
        notify_user(group_request, "REMOVED")
        return redirect('groups')

# HELPERS
def notify_discord_channel(group_request, guild):
    if guild and guild.slug in discord_settings.GUILD_ADMIN_CHANNELS:
        channel = discord_settings.GUILD_ADMIN_CHANNELS[guild.slug]
        send_discord_message(
        channel,
        "%s (%s) has applied to %s. https://auth.kryptedgaming.com/groups/" % (group_request.request_user.discord, group_request.request_user, group_request.request_group)
        )

def notify_user(group_request, type):
    try:
        channel = "#bot"
        send_discord_message(
        channel,
        "Your group request to %s has been %s." % (group_request.request_group, type),
        user=group_request.request_user.id
        )
    except KeyError:
        logger.warning("Please define a #bot channel to notify users of group updates.")
    except Exception as e:
        logger.warning(e)
