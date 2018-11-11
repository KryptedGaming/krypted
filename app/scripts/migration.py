import json, django, datetime, time
from core.models import User, Group, Guild
from modules.discord.models import DiscordUser, DiscordGroup
from modules.discourse.models import DiscourseUser, DiscourseGroup
from games.eveonline.models import EveCharacter, Token

enabled = [
        # stage 1, delete discord/discourse groups after
        # 'auth.user',
        # 'auth.group',
        # stage 2
        # 'discord.discorduser',
        # 'discord.discordgroup',
        # 'discourse.discourseuser',
        # 'discourse.discoursegroup',
        # 'eveonline.token',
        # 'eveonline.evecharacter'
        # stage 3
        # 'group.migration',
        # 'discord.group.migration',
        # 'discourse.group.migration',
        # stage 4
        # 'password.filler',
        'guild.migration',
        ]
users = {}
groups = {}
tokens = {}

with open('/home/auth/development/kryptedauth/scripts/db.json') as f:
    data = json.load(f)

for line in data:
    if line['model'] == 'auth.user':
        users[line['pk']] = line['fields']['username']
    if line['model'] == 'auth.group':
        groups[line['pk']] = line['fields']['name']
    if line['model'] == 'eveonline.token':
        tokens[line['pk']] = line['fields']['character_id']

for line in data:
    fields = line['fields']
    # AUTH.USER
    if line['model'] == 'auth.user' and 'auth.user' in enabled:
        try:
            username = line['fields']['username']
            first_name = line['fields']['first_name']
            last_name = line['fields']['last_name']
            email = line['fields']['email']
            is_active = line['fields']['is_active']
            date_joined = line['fields']['date_joined']
            last_login = line['fields']['last_login']
            User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active,
                date_joined=date_joined,
                last_login=last_login,
                region="US"
            ).save()
        except Exception as e:
            print(e)
    # AUTH.GROUP
    if line['model'] == 'auth.group' and 'auth.group' in enabled:
        try:
            name = fields['name']
            description = "null"
            type = "PRIVATE"
            Group(
                name=name,
                description=description,
                type=type
            ).save()
            time.sleep(1)
        except Exception as e:
            print(line)
            print(e)
    # DISCORD.DISCORDUSER
    if line['model'] == 'discord.discorduser' and 'discord.discorduser' in enabled:
        user=users[fields['user']]
        username = fields['username']
        email = fields['email']
        refresh_token = fields['refresh_token']
        access_token = fields['access_token']
        external_id = line['pk']
        try:
            DiscordUser(
                user=User.objects.get(username=user),
                username=username,
                email=email,
                refresh_token=refresh_token,
                access_token=access_token,
                external_id=external_id
            ).save()
        except Exception as e:
            print(line)
            print(e)
    # DISCORD.DISCORDGROUP
    if line['model'] == 'discord.discordgroup' and 'discord.discordgroup' in enabled:
        external_id = line['pk']
        group = groups[fields['group']]
        DiscordGroup(
            external_id=external_id,
            group=Group.objects.get(name=group)
        ).save()
    # DISCOURSE.DISCOURSEUSER
    if line['model'] == 'discourse.discourseuser' and 'discourse.discourseuser' in enabled:
        external_id = line['pk']
        user=users[fields['auth_user']]
        try:
            DiscourseUser(
                user=User.objects.get(username=user),
                external_id=external_id
            ).save()
        except Exception as e:
            print(user)
            print(e)
    # DISCOURSE.DISCOURSEGROUP
    if line['model'] == 'discourse.discoursegroup' and 'discourse.discoursegroup' in enabled:
        external_id = line['pk']
        group = groups[fields['group']]
        DiscourseGroup(
            external_id=external_id,
            group=Group.objects.get(name=group)
        ).save()
    # EVEONLINE.TOKEN
    if line['model'] == 'eveonline.token' and 'eveonline.token' in enabled:
        character_name=fields['character_name']
        character_id=fields['character_id']
        expiry=fields['expiry']
        character_owner_hash=fields['character_owner_hash']
        expires_in=1119
        access_token=fields['access_token']
        refresh_token=fields['refresh_token']
        user=users[fields['user']]
        Token(
            character_name=character_name,
            character_id=character_id,
            expiry=expiry,
            character_owner_hash=character_owner_hash,
            expires_in=expires_in,
            access_token=access_token,
            refresh_token=refresh_token,
            user=User.objects.get(username=user)
        ).save()
    # EVEONLINE.EVECHARACTER
    if line['model'] == 'eveonline.evecharacter' and 'eveonline.evecharacter' in enabled:
        character_name = line['pk']
        character_portrait = fields['character_portrait']
        user = users[fields['user']]
        token = tokens[fields['token']]
        corporation = fields['corporation']
        character_alt_type=fields['character_alt_type']

        EveCharacter(
            character_name=character_name,
            character_portrait=character_portrait,
            user=User.objects.get(username=user),
            token=Token.objects.get(character_id=token),
            corporation=None,
            character_alt_type=character_alt_type
        ).save()
    # GROUP MIGRATION
    if line['model'] == 'auth.user' and 'group.migration' in enabled:
        user_groups = fields['groups']
        for group in user_groups:
            User.objects.get(username=fields['username']).groups.add(Group.objects.get(name=groups[group]))
    # DISCORD GROUP MIGRATION
    if line['model'] == 'discord.discorduser' and 'discord.group.migration' in enabled:
        user_groups = fields['groups']
        for group in user_groups:
            DiscordUser.objects.get(user=User.objects.get(username=users[fields['user']])).groups.add(DiscordGroup.objects.get(external_id=group))
    # DISCOURSE GROUP MIGRATION
    if line['model'] == 'discourse.discourseuser' and 'discourse.group.migration' in enabled:
        user_groups = fields['groups']
        for group in user_groups:
            DiscourseUser.objects.get(user=User.objects.get(username=users[fields['auth_user']])).groups.add(DiscourseGroup.objects.get(external_id=group))
    # PASSWORD MIGRATION
    if line['model'] == 'auth.user' and 'password.filler' in enabled:
        try:
            password = line['fields']['password']
            username = line['fields']['username']
            user = User.objects.get(username=username)
            user.password = password
            user.save()
        except Exception as e:
            print(e)
# GUILD MIGRATION
if 'guild.migration' in enabled:
    for guild in Guild.objects.all():
        for user in User.objects.all():
            if guild.group in user.groups.all():
                user.guilds.add(guild)
