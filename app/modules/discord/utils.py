from django.conf import settings
import requests

def viewDiscordGroups():
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
    view_groups = requests.get(url, headers={'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN}).json()
    print(view_groups)
    print(url)
    print(headers)

def createDiscordGroup():
    url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
    data={'name': 'test'}
    headers={'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN}
    create_group = requests.post(url,
        data={'name': 'test'},
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        }
    ).json()
    print(create_group)
