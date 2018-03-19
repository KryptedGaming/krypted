from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete, post_save

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import User, Group
        from core.signals import create_group_entity
        post_save.connect(create_group_entity, sender=Group)
