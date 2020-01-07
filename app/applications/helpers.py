from .models import ApplicationTemplate
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)


def get_manageable_application_templates(user):
    if user.has_perm('applications.bypass_required_group_to_manage'):
        logger.debug("Bypass application manger group detected, returning all application templates")
        return ApplicationTemplate.objects.all() 
    else:
        return ApplicationTemplate.objects.filter(
            Q(required_group_to_manage=None) |
            Q(required_group_to_manage__in=user.groups.all())
        )