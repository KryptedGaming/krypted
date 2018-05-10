from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.exceptions import RateLimitException
import logging, requests, json
logger = logging.getLogger(__name__)

class DiscordUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    groups = models.ManyToManyField("DiscordGroup")

    def sanitize(self):
        for group in DiscordGroup.objects.all():
            self.remove_group(group)

    def add_group(self, role):
        """
        Expects a User object and DiscordGroup object.
        Adds the specified role to a user.
        """
        url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  self.id + "/roles/" + str(role.id)
        response = requests.put(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        })
        if response.status_code == 429:
            logger.warning("[MODEL] RATELIMIT to add ROLE [%s] to USER [%s]" % (role.group.name, self.user.username))
            raise RateLimitException
        elif response.status_code == 204:
            logger.info("[MODEL] SUCCESS to add ROLE [%s] to USER [%s]" % (role.group.name, self.user.username))
            self.groups.add(role)
        else:
            logger.error("[MODEL] FAILURE to add ROEL [%s] to USER [%s]: %s" % (role.group.name, self.user.username, response.json()))


    def remove_group(self, role):
        """
        Expects a User object and DiscordGroup object.
        Remove the specified role from a user.
        """
        url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/members/" +  self.id + "/roles/" + str(role.id)
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        })
        if response.status_code == 429:
            logger.warning("[MODEL] RATELIMIT to remove ROLE [%s] from USER [%s]" % (role.group.name, self.user.username))
            raise RateLimitException
        elif response.status_code == 204:
            logger.info("[MODEL] SUCCESS to remove ROLE [%s] from USER [%s]" % (role.group.name, self.user.username))
            self.groups.remove(role)
        else:
            logger.error("[MODEL] FAILURE to remove ROLE [%s] from USER [%s]: %s" % (role.group.name, self.user.username, response.json()))

class DiscordGroup(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """
        Expects a string role_name and a Group object.
        Creates a Discord Group in the auth database, as well as the Discord server.
        """
        # group = kwargs.get('group')
        url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles"
        # Set channel name
        data=json.dumps({'name': self.group.name})
        response = requests.post(url,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
            }
        )
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            logger.info("[MODEL] Discord Group successfully added")
            self.id = response.json()['id']
            super(DiscordGroup, self).save(*args, **kwargs)
        else:
            logger.error("[MODEL] Adding Disord role %s failed with %s : %s" % (group.name, response.status_code, response.json()))

    def delete(self, *args, **kwargs):
        """
        Expects a DiscordGroup object.
        Deletes the Discord Role from our database and the Discord server.
        """
        url = settings.DISCORD_API_ENDPOINT + "/guilds/" + settings.DISCORD_SERVER_ID + "/roles/" + self.id
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + settings.DISCORD_BOT_TOKEN
        })
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 204:
            logger.info("[MODEL] Discord Group successfully removed")
            super(DiscordGroup, self).delete(*args, **kwargs)
        else:
            logger.error("[MODEL] Removing Disord role %s failed with %s" % (role.group.name, response.json()))
