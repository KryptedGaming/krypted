from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.apps import apps 
from django.conf import settings
from .models import Application
import logging 
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Application)
def notify_discord_channel(sender, **kwargs):
    try:
        from django_discord_connector.request import DiscordRequest
        channel = apps.get_app_config(
            'applications').APPLICATIONS_NOTIFICATION_CHANNEL
        application = kwargs.get('instance')
        application_url = reverse('application-detail', kwargs={'pk': application.pk})
        url = f"{settings.SITE_PROTOCOL}{settings.SITE_DOMAIN}{application_url}"

        message = {
            'title': f"New Application - {application.template.name}",
            'fields': [
                {
                    'name' : "Description",
                    'value': f"There is a new application by {application.request_user}"
                },
                {
                    'name' : "View Application",
                    'value': f"[Click here to view the application]({url})"
                },
            ],
        }

        response = DiscordRequest.get_instance().send_channel_message(
            channel, 
            embed=message
        )

    except Exception as e:
        logger.error(f"Failed to notify Discord channel of new application. {e}")
