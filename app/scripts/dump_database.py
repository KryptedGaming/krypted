# DJango imports
from django.core import serializers
# Models from Django
from django.contrib.auth.models import Group as DjangoGroup
from core.models import User, Group, Event, Guild, GroupRequest, GuildApplicationTemplate, GuildApplicationQuestion, GuildApplicationResponse, GuildApplication
from games.eveonline.models import Token, EveCorporation, EveCharacter
#from modules.stats.models import UserStatistic, GuildStatistic, StaffStatistic
from modules.discourse.models import DiscourseUser, DiscourseGroup
from modules.discord.models import DiscordUser, DiscordGroup
# Python imports
import json

model_classes = [
# Core Models
    Group,
    Guild,
    User,
    Event,
    GroupRequest,
    GuildApplicationQuestion,
    GuildApplicationTemplate,
    GuildApplication,
    GuildApplicationResponse,
# Eve Online Models
    Token,
    EveCorporation,
    EveCharacter,
# Stats
#    UserStatistic,
#    GuildStatistic,
#    StaffStatistic,
# Discourse
    DiscourseGroup,
    DiscourseUser,
# Discord
    DiscordGroup,
    DiscordUser,
]

def run():
    d = []
    JSON_Serializer = serializers.get_serializer('json')
    json_serializer = JSON_Serializer()
    for klass in model_classes:
        json_serializer.serialize(klass.objects.all())
        d.extend(json.loads(json_serializer.getvalue()))
    print(json.dumps(d))
