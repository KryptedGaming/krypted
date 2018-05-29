from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.exceptions import RateLimitException
import requests, json, logging
logger = logging.getLogger(__name__)

# Create your models here.
class DiscourseUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    groups = models.ManyToManyField('DiscourseGroup')
    linked = models.NullBooleanField(default=None)

    def __str__(self):
        return self.auth_user.username

    def save(self, *args, **kwargs):
        url = settings.DISCOURSE_BASE_URL + "/users/" + self.auth_user.username.replace(" ", "_") + ".json"
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
        }
        response = requests.get(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        if response.status_code == 200:
            self.id = response.json()['user']['id']
            self.linked = True
            super(DiscourseUser, self).save(*args, **kwargs)

    def add_group(self, group):
        """
        Expects a Discourse Group
        """
        url = settings.DISCOURSE_BASE_URL + "/groups/" + group.id + "/members.json"
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'usernames': self.auth_user.username.replace(" ", "_")
        }
        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.groups.add(group)
            logger.info("[DISCOURSE][MODEL] Added %s to %s" % (self.auth_user.username, group.group.name))
        elif response.status_code == 422:
            self.remove_group(group)
            self.add_group(group)
        else:
            if "already a member" in response.json()['errors']:
                logger.info("got ya")
            logger.error("[DISCOURSE][MODEL] Failed to add %s to %s: %s" % (self.auth_user.username, group.group.name, response.json()))
            return response

    def remove_group(self, group):
        """
        Expects a Discourse Group
        """
        # Remove the Group
        url = settings.DISCOURSE_BASE_URL + "/groups/" + group.id + "/members.json"
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'user_id': self.id
        }
        response = requests.delete(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.groups.remove(group)
            logger.info("[DISCOURSE][MODEL] Removed %s from Discourse Group %s" % (self.auth_user.username, group.group.name))
        else:
            logger.info("[DISCOURSE][MODEL] Failed to remove %s from Discourse Group %s: %s" % (self.auth_user.username, group.group.name, response.json()))

class DiscourseGroup(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.group.name

    def save(self, *args, **kwargs):
        url = settings.DISCOURSE_BASE_URL + "/admin/groups"
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'group[name]': self.group.name
        }
        response = requests.post(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            logger.info("[MODEL] Discourse Group successfully added")
            response = dict(response.json())
            self.id = response['basic_group']['id']
            super(DiscourseGroup, self).save(*args, **kwargs)
        else:
            logger.info("[MODEL] Discourse Group addition failed with %s" % response.json())

    def delete(self, *args, **kwargs):
        url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + self.id + ".json"
        logger.info(url)
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
        }
        response = requests.delete(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            logger.info("[MODEL] Discourse Group succesfully deleted")
            super(DiscourseGroup, self).delete(*args, **kwargs)
        else:
            logger.info("[MODEL] Discourse Group removal failed with %s" % str(response))
