# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
# INTERNAL IMPORTS
from modules.guilds.models import Guild
# MISC
import logging
logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'guilds/guilds.html', context)

@login_required
def user_list(request):
    context = {'guilds': Guild.objects.all()}
    return render(request, 'guilds/guild_user_list.html', context)

@login_required
@permission_required('guilds.change_guild')
def remove_guild_user(request, guild_id, user_id):
    guild = Guild.objects.get(pk=guild_id)
    user = User.objects.get(pk=user_id)
    guild.users.remove(user)
    messages.add_message(request, messages.SUCCESS, '%s has been removed from %s' % (user, guild))
    return redirect('guild-users')
    