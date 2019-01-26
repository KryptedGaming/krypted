from django.apps import apps
import json, requests
discourse_settings = apps.get_app_config('discourse')
class DiscourseClient:
    """
    Discourse API Client
    Used to interact with the Discourse forum
    """
    @staticmethod
    def get_discourse_user(username):
        url = discourse_settings.DISCOURSE_BASE_URL + "/users/" + username.replace(" ", "_") + ".json"
        data = {
            'api_key': discourse_settings.DISCOURSE_API_KEY,
            'api_username': 'system',
        }
        response = requests.get(
            url=url,
            data=data
        )
        return response

    @staticmethod
    def get_discourse_users(self):
        pass

    @staticmethod
    def add_group_to_discourse_user(username, group_id):
        url = discourse_settings.DISCOURSE_BASE_URL + "/groups/" + str(group_id) + "/members.json"
        data = {
            'api_key': discourse_settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'usernames': username.replace(" ", "_")
        }
        response = requests.put(url=url, data=data)
        return response

    @staticmethod
    def remove_group_from_discourse_user(user_external_id, group_id):
        url = discourse_settings.DISCOURSE_BASE_URL + "/groups/" + str(group_id) + "/members.json"
        data = {
            'api_key': discourse_settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'user_id': user_external_id
        }
        response = requests.delete(url=url, data=data)
        return response

    @staticmethod
    def add_group_to_discourse_server(group_name):
        url = discourse_settings.DISCOURSE_BASE_URL + "/admin/groups"
        data = {
            'api_key': discourse_settings.DISCOURSE_API_KEY,
            'api_username': 'system',
            'group[name]': group_name
        }
        response = requests.post(url=url, data=data)
        return response

    @staticmethod
    def remove_group_from_discourse_server(group_external_id):
        url = discourse_settings.DISCOURSE_BASE_URL + "/admin/groups/" + str(group_external_id) + ".json"
        data = {
            'api_key': discourse_settings.DISCOURSE_API_KEY,
            'api_username': 'system',
        }
        response = requests.delete(url=url, data=data)
        return response
