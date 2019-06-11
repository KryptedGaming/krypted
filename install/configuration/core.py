from django.apps import AppConfig, apps
from django.db.models.signals import m2m_changed, pre_delete, post_save, post_migrate

class CoreConfig(AppConfig):
    name = 'core'

    GOOGLE_ANALYTICS_CODE = ''
    SITE_TITLE = ''
    SITE_LOGO = ''

    REGIONS = (
        ("NA", "North America"),
        ("EU", "Europe"),
        ("OC", "Oceania & Asias")
    )

    def ready(self):
        from django.contrib.auth.models import User, Group
        from core.signals import global_user_add, global_group_add, user_group_change_discord_notify, user_group_change_check_dependent_groups
        post_save.connect(global_user_add, sender=User)
        post_save.connect(global_group_add, sender=Group)
        m2m_changed.connect(user_group_change_check_dependent_groups, sender=User.groups.through)
        if apps.is_installed('modules.discord'):
            m2m_changed.connect(user_group_change_discord_notify, sender=User.groups.through)