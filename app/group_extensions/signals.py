from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group
from .models import GroupTrigger
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import logging
logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=User.groups.through)
def trigger_group_extensions(sender, **kwargs):
    def call():
        user = kwargs.get('instance')
        action = kwargs.get('action')
        pk_set = kwargs.get('pk_set')

        if action == "post_add":
            groups = Group.objects.filter(pk__in=list(pk_set))
            for group in groups:
                try:
                    trigger = group.trigger
                    if trigger.add_groups_on_trigger:
                        user.groups.add(*trigger.target_groups.all())
                except ObjectDoesNotExist:
                    pass

        if action == "post_remove":
            groups = Group.objects.filter(pk__in=pk_set)
            for group in groups:
                try:
                    trigger = group.trigger
                    if trigger.remove_groups_on_trigger:
                        user.groups.remove(*trigger.target_groups.all())
                except ObjectDoesNotExist:
                    pass

    transaction.on_commit(call)
