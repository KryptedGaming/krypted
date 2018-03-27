from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save
from modules.slack.tasks import *
from modules.slack.models import *
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=User.groups.through)
def user_group_change(sender, **kwargs):
    logger.info("Groups changed for user. Updating slack channels.")
    user = kwargs.get('instance')
    action = str(kwargs.get('action'))
    try:
        user = SlackUser.objects.get(user=user)
        groups = []
        for pk in kwargs.get('pk_set'):
            groups.append(Group.objects.get(pk=pk))
        for group in groups:
            if action == "post_remove":
                try:
                    channel = SlackChannel.objects.get(groups__name__in=[group])
                    remove_slack_user_from_channel.apply_async(args=[channel.slack_id, user.slack_id])
                    # remove user
                except:
                    pass # no action needed
            elif action == "post_add":
                try:
                    channel = SlackChannel.objects.get(groups__name__in=[group])
                    add_slack_user_to_channel.apply_async(args=[channel.slack_id, user.slack_id])
                except:
                    pass # no action needed
    except Exception as e:
        logger.info("Failed to updated Slack channels. %s" % e)
