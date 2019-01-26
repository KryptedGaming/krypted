from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import User, Group
        from core.signals import global_user_add, global_group_add
        post_save.connect(global_user_add, sender=User)
        post_save.connect(global_group_add, sender=Group)
