from django.apps import AppConfig


class GroupExtensionsConfig(AppConfig):
    name = 'group_extensions'
    url_slug = 'groups'

    def ready(self):
        from django.db.models.signals import m2m_changed
        from .models import User
        from .signals import trigger_group_extensions

        m2m_changed.connect(trigger_group_extensions,
                            sender=User.groups.through)
