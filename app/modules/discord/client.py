from app.conf import discord as discord_settings
import json, requests
class DiscordClient:
    """
    Discord API Client class
    Used to interact with the Discord server
    """
    @staticmethod
    def activate():
        from discord.ext import commands
        prefix = "?"
        bot = commands.Bot(command_prefix=prefix)
        bot.run(discord_settings.DISCORD_BOT_TOKEN)

    @staticmethod
    def get_discord_user(discord_user_id):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/members/" +  str(discord_user_id)
        response = requests.get(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
        })
        return response

    @staticmethod
    def get_discord_users(self):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/members/"
        response = requests.get(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
        })
        return response

    @staticmethod
    def add_group_to_discord_user(discord_user_id, discord_group_id):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/members/" +  str(discord_user_id) + "/roles/" + str(discord_group_id)
        response = requests.put(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
        })
        return response

    @staticmethod
    def remove_group_from_discord_user(discord_user_id, discord_group_id):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/members/" +  str(discord_user_id) + "/roles/" + str(discord_group_id)
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
        })
        return response

    @staticmethod
    def add_group_to_discord_server(group_name):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/roles"
        data=json.dumps({'name': group_name})
        response = requests.post(url,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
            }
        )
        return response

    @staticmethod
    def remove_group_from_discord_server(discord_group_id):
        url = discord_settings.DISCORD_API_ENDPOINT + "/guilds/" + discord_settings.DISCORD_SERVER_ID + "/roles/" + str(discord_group_id)
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
        })
        return response

    @staticmethod
    def send_message(discord_channel, message):
        channel_id = discord_settings.DISCORD_CHANNEL_IDS[channel]
        print(channel_id)
        url = discord_settings.DISCORD_API_ENDPOINT + "/channels/" + str(channel_id) + "/messages"
        data=json.dumps({'content': message})
        response = requests.post(url,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bot ' + discord_settings.DISCORD_BOT_TOKEN
            }
        )
        return response
