from django.apps import AppConfig
import os
import logging


logger = logging.getLogger(__name__)

class ApplicationsConfig(AppConfig):
    name = 'applications'
    verbose_name = "Applications"
    url_slug = 'applications'

    APPLICATIONS_NOTIFICATION_CHANNEL = os.environ.get(
        'APPLICATIONS_NOTIFICATION_CHANNEL', None)

    def ready(self):
        from django.db.models.signals import post_save
        from .models import Application
        from .signals import notify_discord_channel
        from django.conf import settings 
        if 'django_discord_connector' in settings.INSTALLED_APPS and self.APPLICATIONS_NOTIFICATION_CHANNEL:
            logger.info("Application notifications are enabled")
            post_save.connect(notify_discord_channel, sender=Application)
