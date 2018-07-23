from modules.discord.models import DiscordUser
from modules.discourse.models import DiscourseUser
from games.eveonline.models import EveCharacter
from core.models import Profile
def get_main_eve_character(user):
    try:
        response = EveCharacter.objects.filter(user=user)[0].get_absolute()
    except:
        response = None

    return response

def user_service_status(user):
    status = {}
    discord = DiscordUser.objects.filter(user=user).first()
    discourse = DiscourseUser.objects.filter(auth_user=user).first()
    groups = set(user.groups.all())
    discord_groups = set()
    discourse_groups = set()
    # build discord groups
    if discord:
        for group in discord.groups.all():
            discord_groups.add(group.group)
    if discourse:
        for group in discourse.groups.all():
            discourse_groups.add(group.group)
    status['discord'] = groups == discord_groups
    status['discourse'] = groups == discourse_groups
    return status

def hard_sync(user):
    groups = user.groups.all()
    for group in groups:
        user.groups.remove(group)
    for group in groups:
        user.groups.add(group)

def get_user_profile(user):
    return Profile.objects.get(user=user)
