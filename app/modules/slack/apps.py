from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save

class SlackConfig(AppConfig):
    name = 'modules.slack'

    def ready(self):
        pass
        # from django.contrib.auth.models import User, Group
        # from modules.slack.signals import user_group_change
        # m2m_changed.connect(user_group_change, sender=User.groups.through)
