# DJANGO IMPORTS
from django.apps import apps
from django.contrib.auth.models import Group
# MISC
import logging

logger = logging.getLogger(__name__)

# FUNCTIONS
def discord_notify_user(user, group_id, type, **kwargs):
    from modules.discord.models import DiscordChannel
    from modules.discord.tasks import send_discord_channel_message
    from django.core.exceptions import ObjectDoesNotExist
    try:
        discord_channel = DiscordChannel.objects.get(type="BOT")
    except ObjectDoesNotExist:
        logger.warning("Please specify a BOT discord channel for application user notifications.")
        return
    if type == "submit":
        send_discord_channel_message(
        discord_channel.name,
        "Thank you for submitting your %s application. Please wait up to 48 hours to be assigned a recruiter." % Group.objects.get(id=group_id),
        user=user.id
        )
    elif type == "accepted":
        send_discord_channel_message(
        discord_channel.name,
        "Congratulations, your application to %s has been **ACCEPTED.** Welcome aboard, DM your recruiter for the next step." % Group.objects.get(id=group_id),
        user=user.id
        )
    elif type == "rejected":
        send_discord_channel_message(
        discord_channel.name,
        "Sorry, your application to %s has been **REJECTED.** DM your recruiter for details." % Group.objects.get(id=group_id),
        user=user.id
        )
    elif type == "assigned":
        recruiter = kwargs.get('recruiter')
        send_discord_channel_message(
        discord_channel.name,
        "Your application to %s has been assigned to **%s**. DM them if you have questions." % (Group.objects.get(id=group_id), recruiter.info.discord),
        user=user.id
        )

def discord_notify_recruitment_channel(user, group_id, type):
    from modules.discord.models import DiscordChannel
    from modules.discord.tasks import send_discord_channel_message
    from django.core.exceptions import ObjectDoesNotExist
    try:
        discord_channel = DiscordChannel.objects.get(type="HR")
    except ObjectDoesNotExist:
        logger.warning("Please specify a BOT discord channel for application user notifications.")
        return
    try:
        discord_channel = DiscordChannel.objects.get(type="HR")
    except ObjectDoesNotExist:
        logger.warning("Please specify a HR discord channel for application user notifications.")
        return
    if type == "submit":
        send_discord_channel_message(
        discord_channel.name,
        "%s has submitted an %s application. Please add a :white_check_mark: if you intend on handling it." % (user.discord_user, Group.objects.get(id=group_id)),
        group=Group.objects.get(id=group_id).id
        )
