from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.db import transaction
from core.models import GroupEntity
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Group)
def create_group_entity(sender, **kwargs):
    def call():
        group = kwargs.get('instance')
        GroupEntity.objects.get_or_create(group=group)
        logger.info("Group %s added. Adding to Core group management." % group.name)
    transaction.on_commit(call)


