# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.apps import apps
# LOCAL IMPORTS
from core.forms import LoginForm, RegisterForm, ProfileForm
from core.decorators import login_required, services_required, staff_required
from core.models import *
# from core.utils import get_main_eve_character
# # MODULE IMPORTS
# if apps.is_installed('modules.slack'):
#     from modules.slack.models import SlackUser
# from modules.discord.models import DiscordUser
# from modules.discourse.models import DiscourseUser
# # GAME IMPORTS
# from games.eveonline.models import EveCharacter
# OTHER IMPORTS
import logging
logger = logging.getLogger(__name__)

## BASE
@login_required
def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'base/dashboard.html', context)

@login_required
@services_required
def guilds(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'base/guilds.html', context)

@login_required
@services_required
@staff_required
def applications(request):
    context = {'applications': GuildApplication.objects.all()}
    return render(request, 'base/applications.html', context)

@login_required
@services_required
def groups(request, **kwargs):
    context = {}
    groups = []
    # PERMISSIONS
    context['manage'] = request.user.has_perm('core.manage_group_requests')
    context['audit'] = request.user.has_perm('core.audit_group_requests')

    # STANDARD GROUP VIEW
    for group in Group.objects.order_by('guild'):
        if group.type == "PUBLIC" :
            if not group.guild:
                groups.append({
                    'group': group,
                    'requested': request.user.has_group_request(group)
                })
            elif group.guild in request.user.guilds.all():
                groups.append({
                    'group': group,
                    'requested': request.user.has_group_request(group)
                })
        elif group.type == "PROTECTED":
            if group.guild in request.user.guilds.all():
                groups.append({
                    'group': group,
                    'user_has_group': (group in request.user.groups.all()),
                    'requested': request.user.has_group_request(group)
                })
        elif group.type == "PRIVATE":
            pass # hide private groups
        else:
            logger.error("Received group without defined types: %s" % group)
    context['groups'] = groups

    # PENDING VIEW
    if context['manage']:
        group_requests = []
        for group_request in GroupRequest.objects.filter(response_action="Pending"):
            if not group_request.request_group.managers.all() or request.user in group_request.request_group.managers.all():
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

    return render(request, 'base/groups.html', context)

# ## MISC
def view_members(request):
    # members = {}
    # for user in User.objects.all():
    #     members[user.username] = {}
    #     members[user.username]['discourse'] = DiscourseUser.objects.filter(auth_user=user).exists()
    #     members[user.username]['discord'] = DiscordUser.objects.filter(user=user).exists()
    #     if members[user.username]['discord']:
    #         members[user.username]['discord_user'] = DiscordUser.objects.get(user=user).username
    #     members[user.username]['eve'] = Group.objects.get(name=settings.EVE_ONLINE_GROUP) in user.groups.all()
    #     members[user.username]['eve_character'] = get_main_eve_character(user)
    #     members[user.username]['wow'] = Group.objects.get(name=settings.WORLD_OF_WARCRAFT_GROUP) in user.groups.all()
    # context['members'] = members
    return render(request, 'base/members.html', context=context)
