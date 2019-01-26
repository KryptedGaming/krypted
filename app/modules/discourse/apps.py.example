from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save

class DiscourseConfig(AppConfig):
    name = 'modules.discourse'
    # DISCOURSE SETTINGS
    DISCOURSE_AUTOMATIC_GROUPS = ['admins', 'moderators', 'staff', 'trust_level_0', 'trust_level_1', 'trust_level_2', 'trust_level_3', 'trust_level_4']
    # USER SETTINGS
    DISCOURSE_BASE_URL = ""
    DISCOURSE_API_KEY = ""
    DISCOURSE_API_USERNAME = ""
    DISCOURSE_SSO_SECRET = ""

    def ready(self):
        from django.contrib.auth.models import User, Group
        from modules.discourse.signals import user_group_change, global_group_add, global_group_remove
        m2m_changed.connect(user_group_change, sender=User.groups.through)
        pre_delete.connect(global_group_remove, sender=Group)
        post_save.connect(global_group_add, sender=Group)
