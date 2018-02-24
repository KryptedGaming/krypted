from django.conf import settings
from modules.discourse.models import DiscourseGroup
from django.contrib.auth.models import Group, User
import requests, json, logging
logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

# Group Management
def add_discourse_group(group):
    """
    Expects a Group object.
    """
    url = settings.DISCOURSE_BASE_URL + "/admin/groups"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'group[name]': group.name
    }
    response = requests.post(url=url, data=data)
    if response.status_code == 429:
        response = dict(response.json())
        raise RateLimitException()
    response = dict(response.json())
    try:
        discourse_group = DiscourseGroup(role_id=response['basic_group']['id'], group=group)
        discourse_group.save()
    except:
        pass

def remove_discourse_group(group):
    """
    Expects a DiscourseGroup object.
    """
    url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + str(group.role_id)
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
    }
    try:
        response = requests.delete(url=url, data=data)
        group.delete()
    except:
        if response.status_code == 429:
            response = dict(response.json())
            raise RateLimitException()
        else:
            pass

def update_discourse_groups():
    """
    Cleans up all DiscourseGroups that don't exist as Groups, adds new ones that should.
    Made for tasks.py, ran every now and then.
    Rate Limit Information - 7 + Group.objects.all()*2
    """
    # Clean up all groups that shouldn't exist
    url = settings.DISCOURSE_BASE_URL + "/admin/groups.json?" + "api_key=" + settings.DISCOURSE_API_KEY + "&" + "api_username=" + settings.DISCOURSE_API_USERNAME
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
    }
    response = requests.get(url=url, data=data)
    if response.status_code == 429:
        response = response.json()
        raise RateLimitException()
    else:
        for json_group_response in response.json():
            group_name = json_group_response['name']
            if Group.objects.filter(name=group_name).count() == 0 and group_name not in settings.DISCOURSE_AUTOMATIC_GROUPS:
                temporary_group = DiscourseGroup(role_id=json_group_response['id'])
                remove_discourse_group(temporary_group)

    # Add ones that should exist on Discourse
    groups_to_add = []
    for group in Group.objects.all():
        to_add = True
        for json_group_response in response.json():
            group_name = json_group_response['name']
            if (group_name == group.name):
                to_add = False
        if to_add:
            groups_to_add.append(group)
    for group in groups_to_add:
        add_discourse_group(group)

# User Group Management
def get_discourse_user(user):
    url = settings.DISCOURSE_BASE_URL + "/users/" + user.username.replace(" ", "_") + ".json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'usernames': user.username.replace(" ", "_")
    }
    response = requests.get(url=url, data=data)
    if response.status_code == 429:
        response = dict(response.json())
        raise RateLimitException()
    try:
        response_body = response.json()
        return response_body['user']['id']
    except:
        logger.info("%s" % response)

def add_user_to_discourse_group(user, group):
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'usernames': user.username.replace(" ", "_")
    }
    try:
        response = requests.put(url=url, data=data)
    except:
        if response.status_code == 429:
            response = dict(response.json())
            raise RateLimitException()
        else:
            logger.info("%s" % response.json())


def remove_user_from_discourse_group(user, group):
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'user_id': get_discourse_user(user)
    }
    try:
        response = requests.delete(url=url, data=data)
    except:
        if response.status_code == 429:
            response = dict(response.json())
            raise RateLimitException()
        else:
            logger.info("%s" % response.json())
