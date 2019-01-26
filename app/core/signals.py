# DJANGO IMPORTS
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
# LOCAL IMPOTRS
from core.models import UserInfo, GroupInfo
# MISC
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def global_user_add(sender, **kwargs):
    def call():
        user = kwargs.get('instance')
        logger.info("[SIGNAL] Creating UserInfo() for %s" % user)
        if (kwargs.get('created')):
            UserInfo(user=user).save()
    transaction.on_commit(call)

@receiver(post_save, sender=Group)
def global_group_add(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        logger.info("[SIGNAL] Creating GroupInfo() for %s" % group)
        if (kwargs.get('created')):
            GroupInfo(group=group).save()
    transaction.on_commit(call)
