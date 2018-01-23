from django.conf import settings
from modules.discourse.models import DiscourseGroup
from django.contrib.auth.models import Group, User
import requests
import json

# Group Management
def addGroup(group):
    """
    Expects a Group object.
    """
    url = settings.DISCOURSE_BASE_URL + "/admin/groups"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'group[name]': group.name
    }
    add_group = dict(requests.post(url=url, data=data).json())
    discourse_group = DiscourseGroup(role_id=add_group['basic_group']['id'], group=group)
    discourse_group.save()

def removeGroup(group):
    """
    Expects a DiscourseGroup object.
    """
    url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + str(group.role_id)
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
    }
    remove_group = requests.delete(url=url, data=data)
    print(remove_group)
    group.delete()

def updateGroups():
    """
    Cleans up all DiscourseGroups that don't exist as Groups, adds new ones that should.
    Made for tasks.py, ran every now and then.
    """
    # Clean up all groups that shouldn't exist
    url = settings.DISCOURSE_BASE_URL + "/admin/groups.json?" + "api_key=" + settings.DISCOURSE_API_KEY + "&" + "api_username=" + settings.DISCOURSE_API_USERNAME
    get_groups = requests.get(url=url).json()
    for json_group_response in get_groups:
        to_check = json_group_response['name']
        if Group.objects.filter(name=to_check).count() == 0 and to_check not in settings.DISCOURSE_AUTOMATIC_GROUPS:
            temporary_group = DiscourseGroup(role_id=json_group_response['id'])
            removeGroup(temporary_group)

    # Add ones that should exist on Discourse
    groups_to_add = []
    for group in Group.objects.all():
        to_add = True
        for json_group_response in get_groups:
            if (json_group_response['name'] == group.name):
                to_add = False
        if to_add:
            groups_to_add.append(group)
    for group in groups_to_add:
        addGroup(group)

# User Group Management
def getUser(user):
    url = settings.DISCOURSE_BASE_URL + "/users/" + user.username + ".json"
    try:
        get_id = requests.get(url=url).json()
        return get_id['user']['id']
    except:
        print("USER IS NOT SIGNED UP ON DISCOURSE")

def addUserToGroup(user, group):
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'usernames': user.username
    }
    try:
        add_user = requests.put(url=url, data=data).json()
        print(add_user)
    except:
        print("ERROR ADDING USER TO GROUP")

def removeUserFromGroup(user, group):
    url = settings.DISCOURSE_BASE_URL + "/groups/" + group.role_id + "/members.json"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'user_id': getUser(user)
    }
    try:
        remove_user = requests.delete(url=url, data=data).json()
        print("REMOVE USER RESPONSE:")
        print(remove_user)
    except:
        print("ERROR ADDING USER TO GROUP")
