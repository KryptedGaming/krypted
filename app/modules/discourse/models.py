from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
import requests, json, logging
logger = logging.getLogger(__name__)

# Create your models here.
class DiscourseUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField('DiscourseGroup')

    def __str__(self):
        return self.auth_user.username

    def add_group(self, group):
        """
        Expects a Discourse Group
        """
        url = settings.DISCOURSE_BASE_URL + "/groups/" + group.id + "/members.json"
        logger.info(url)
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'usernames': self.auth_user.username.replace(" ", "_")
        }
        logger.info(data['usernames'])
        response = requests.put(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
        elif response.status_code == 200:
            self.auth_user.groups.add(group.group)
            logger.info("[DISCOURSE][MODEL] Added %s to %s" % (self.auth_user.username, group.group.name))
        else:
            logger.error("[DISCOURSE][MODEL] Failed to add %s to %s: %s" % (self.auth_user.username, group.group.name, response.json()))

    def remove_group(self, group):
        """
        Expects a Discourse Group
        """
        url = settings.DISCOURSE_BASE_URL + "/groups/" + group.id + "/members.json"
        data = {
            'api_key': settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'user_id': self.id
        }
        response = requests.delete(url=url, data=data)
        if response.status_code == 429:
            raise RateLimitException
            self.auth_user.groups.remove(group.group)
        elif response.status_code == 200:
            logger.info("[DISCOURSE][MODEL] Remove %s from Discourse Group %s" % (self.auth_user.username, group.group.name))

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
        url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + str(self.id)
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
            logger.info("[MODEL] Discourse Group removal failed with %s" % response.json())
