from django.conf import settings
from modules.discourse.models import DiscourseGroup
import requests
import json

# Group Management
def addGroup(group):
    url = settings.DISCOURSE_BASE_URL + "/admin/groups"
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
        'group[name]': group.name
    }
    add_group = requests.post(url=url, data=data)
    print(requests.request('POST', url, params=data))
    discourse_group = DiscourseGroup(id=add_group['id'], group=group)
    discourse_group.save()

def removeGroup(group):
    url = settings.DISCOURSE_BASE_URL + "/admin/groups/" + group.id
    data = {
        'api_key': settings.DISCOURSE_API_KEY,
        'api_username': 'system',
    }
    remove_group = requests.delete(url=url, data=data)
    group.delete()

# User Group Management
def addUserToGroup():
    pass
def removeUserFromGroup():
    pass
