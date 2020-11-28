import logging
from django.db.utils import OperationalError, ProgrammingError
logger = logging.getLogger(__name__)


class NotificationHandler(logging.Handler):
    def emit(self, record):
        from django.contrib.auth.models import User
        from notifications import notify
        from notifications.models import Notification

        message = record.getMessage()
        if record.exc_text:
            message += "\n\n"
            message = message + record.exc_text

        notification_title_level = record.levelname.title()
        try:
            users = User.objects.filter(is_superuser=True).distinct()

            for user in users:
                notify.send(
                    user,
                    recipient=user,
                    level=record.levelname,
                    verb=f"System {notification_title_level}",
                    description=f"{message}",
                    public=False,
                )
        except OperationalError:
            pass # in migration
        except ProgrammingError:
            pass # in migration