from django.conf import settings
from modules.discord.models import DiscordRole, DiscordToken
import requests
import json

def viewDiscordGroups():
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
    view_groups = requests.get(url, headers={'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN}).json()
    print(view_groups)
    print(url)

def addDiscordGroup(group):
    """
    Expects a string role_name and a Group object.
    Creates a Discord Group in the auth database, as well as the Discord server.
    """
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
    # Set channel name
    data=json.dumps({'name': group.name})
    create_group = requests.post(url,
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        }
    ).json()
    print(create_group)
    role = DiscordRole(role_id=create_group['id'], group=group)
    role.save()
    return role

def removeDiscordGroup(role):
    """
    Expects a DiscordRole object.
    Deletes the Discord Role from our database and the Discord server.
    """
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles/" + str(role.role_id)
    delete_group = requests.delete(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    role.delete()
    print(delete_group)

def addDiscordGroupToUser(user, role):
    """
    Expects a User object and DiscordRole object.
    Adds the specified role to a user.
    """
    discord_id = DiscordToken.objects.get(user=user).userid
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  discord_id + "/roles/" + str(role.role_id)
    add_group_to_user = requests.put(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    print(add_group_to_user)

def removeDiscordGroupFromUser(user, role):
    """
    Expects a User object and DiscordRole object.
    Remove the specified role from a user.
    """
    discord_id = DiscordToken.objects.get(user=user).userid
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  discord_id + "/roles/" + str(role.role_id)
    remove_group_to_user = requests.delete(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
    })
    print(remove_group_to_user)

def getUserRoles(user):
    """
    Expects a User object.
    Returns an array of roles that the user currently has
    """
    discord_id = DiscordToken.objects.get(user=user).userid
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" + str(discord_id)
    view_user_roles = dict(requests.get(url, headers={'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN}).json())
    return view_user_roles['roles']

def cleanUserRoles(user):
    """
    Expects a User object.
    Cleans the roles that don't exist for a User on Krypted auth.
    """
    roles = getUserRoles(user)
    for role in list(roles):
        # clean roles that dont exist
        if DiscordRole.objects.filter(role_id=role).count() == 0:
            role = DiscordRole(role_id=role)
            removeDiscordGroupFromUser(user, role)
        # clean roles that user sholdn't have
        else:
            role = DiscordRole.objects.get(role_id=role)
            if role.group not in user.groups.all():
                removeDiscordGroupFromUser(user, role)

def syncUser(user):
    """
    Expects a User object.
    Syncs a single user.
    """
    if DiscordToken.objects.filter(user=user).count() > 0:
        cleanUserRoles(user)
        for group in user.groups.all():
            role_to_add = DiscordRole.objects.get(group=group)
            addDiscordGroupToUser(user, role_to_add)
    else:
        pass
