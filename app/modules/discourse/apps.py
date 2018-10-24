from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save

class DiscourseConfig(AppConfig):
    name = 'modules.discourse'

    def ready(self):
        from core.models import User, Group
        from modules.discourse.signals import user_group_change, global_group_add, global_group_remove
        m2m_changed.connect(user_group_change, sender=User.groups.through)
        pre_delete.connect(global_group_remove, sender=Group)
        post_save.connect(global_group_add, sender=Group)
