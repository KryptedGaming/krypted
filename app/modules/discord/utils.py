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
