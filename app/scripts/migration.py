# PYTHON IMPORTS
import json, django, datetime, time, traceback, sys
# DJANGO MODEL IMPORTS
from django.contrib.auth.models import Group, Permission, User
# CORE MODEL IMPORTS
from core.models import GroupInfo, GroupRequest, SocialMedia, UserInfo
# MODULE MODEL IMPORTS
from modules.discord.models import DiscordChannel, DiscordGroup, DiscordUser
from modules.discourse.models import DiscourseGroup, DiscourseUser
from modules.guilds.models import Guild, GuildApplication, GuildApplicationQuestion, GuildApplicationResponse, GuildApplicationTemplate
from modules.engagement.models import Event, Survey
from modules.eveonline.models import EveToken, EveCharacter, EveCorporation


enabled = [
        # stage 1, delete discord/discourse groups after
        'core.user',
        'core.group',
        'core.event',
        'core.guild',
        'core.guildapplication',
        'core.guildapplicationquestion',
        'core.guildapplicationresponse',
        'core.guildapplicationtemplate',
        # stage 2
        'discord.discorduser',
        'discord.discordgroup',
        'discourse.discourseuser',
        'discourse.discoursegroup',
        'eveonline.evecorporation',
        'eveonline.token',
        'eveonline.evecharacter'
        ]
users = {}
groups = {}
tokens = {}

def run():
    with open('/home/auth/development/config/db.json') as f:
        data = json.load(f)

    for line in data:
        if line['model'] == 'core.user':
            users[line['pk']] = line['fields']['username']
        if line['model'] == 'core.group':
            groups[line['pk']] = line['fields']['description']
        if line['model'] == 'core.guild':
            if 'eve' == line['fields']['slug']:
                eve = Guild.objects.get(slug='eve')
                eve.delete()
                eve.pk = line['pk']
                eve.save()
        if line['model'] == 'eveonline.character':
            character_tokens[line['pk']] = line['fields']['token']

    for line in data:
        print(" >>> " + str(line))
        fields = line['fields']
        # CORE.USER
        if line['model'] == 'core.user' and 'core.user' in enabled:
            try:
                # TODO: user_permissions, groups, guilds
                # User Fields
                pk = line['pk']
                username = fields['username']
                first_name = fields['first_name']
                last_name = fields['last_name']
                email = fields['email']
                is_active = fields['is_active']
                is_staff= fields['is_staff']
                is_superuser= fields['is_superuser']
                date_joined = fields['date_joined']
                last_login = fields['last_login']
                user_groups = fields['groups']
                guilds = fields['guilds']
                # User Info Fields
                region = fields['region']
                age = fields['age']
                biography = fields['biography']
                avatar = fields['avatar']
                activation_key = fields['activation_key']
                secret = fields['secret']
                password = fields['password']
                user = User(
                    pk=pk,
                    password=password,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=is_active,
                    is_staff=is_staff,
                    date_joined=date_joined,
                    last_login=last_login,
                )
                user.save()
                if user_groups:
                    user.groups.set([Group.objects.get(pk=x) for x in user_groups])
                if guilds:
                    for g in [Guild.objects.get(pk=x) for x in guilds]:
                        g.users.add(user)
                info = user.info
                info.region = region
                info.age = age
                info.biography = biography
                info.avatar = avatar
                info.activation_key = activation_key
                info.secret = secret
                info.save()
            except Exception as e:
                traceback.print_exception(exc_type,exc_value,exc_traceback)
                print(line)
                print(e)
        # CORE.GROUP
        if line['model'] == 'core.group' and 'core.group' in enabled:
            try:
                pk = line['pk']
                name = fields['description']
                description = fields['description']
                type = fields['type']
                managers = fields['managers']
                group = Group(
                    pk=pk,
                    name=description
                )
                group.save()
                info = group.info
                info.description = description
                info.type = type
                if managers:
                    info.managers.set([User.objects.get(pk=x) for x in managers])
                info.save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.EVENT
        if line['model'] == 'core.event' and 'core.event' in enabled:
            try:
                pk = line['pk']
                name = fields['name']
                registrants = fields['registrants']
                participants = fields['participants']
                description = fields['description']
                guild = fields['guild']
                guild_object = None
                if guild:
                    guild_object = Guild.objects.get(pk=guild)
                user = users[fields['user']]
                start_datetime = fields['start_datetime']
                end_datetime = fields['end_datetime']
                password = fields['password']
                value = fields['value']
                e = Event(
                    pk=pk,
                    name=name,
                    description=description,
                    guild=guild_object,
                    user=User.objects.get(username=user),
                    password=password,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    value=value,
                )
                e.save()
                if registrants:
                    e.registrants.set([User.objects.get(pk=x) for x in registrants])
                if participants:
                    e.participants.set([User.objects.get(pk=x) for x in participants])
                e.save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.GUILD
        if line['model'] == 'core.guild' and 'core.guild' in enabled:
            try:
                pk=line['pk']
                name=fields['name']
                group=fields['group']
                slug=fields['slug']
                date_formed=fields['date_formed']
                image=fields['image']
                Guild(
                    pk=pk,
                    name=name,
                    default_group=Group.objects.get(pk=group),
                    slug=slug,
                    date_formed=date_formed,
                    image=image,
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.GUILDAPPLICATION
        if line['model'] == 'core.guildapplication' and 'core.guildapplication' in enabled:
            try:
                pk=line['pk']
                template=fields['template']
                request_user=users[fields['request_user']]
                request_date=fields['request_date']
                status=fields['status']
                response_date=fields['response_date']
                response_user=fields['response_user']
                response_user_object = None
                if response_user:
                    response_user_object = User.objects.get(pk=response_user)
                GuildApplication(
                    pk=pk,
                    template=GuildApplicationTemplate.objects.get(pk=template),
                    request_user=User.objects.get(username=request_user),
                    request_date=request_date,
                    status=status,
                    response_user=response_user_object,
                    response_date=response_date
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.GUILDAPPLICATIONQUESTION
        if line['model'] == 'core.guildapplicationquestion' and 'core.guildapplicationquestion' in enabled:
            try:
                pk=line['pk']
                name=fields['name']
                type=fields['type']
                help_text=fields['help_text']
                choices=fields['choices']
                GuildApplicationQuestion(
                    pk=pk,
                    name=name,
                    type=type,
                    help_text=help_text,
                    choices=choices
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.GUILDAPPLICATIONRESPONSE
        if line['model'] == 'core.guildapplicationresponse' and 'core.guildapplicationresponse' in enabled:
            try:
                pk=line['pk']
                question=fields['question']
                response=fields['response']
                application=fields['application']
                GuildApplicationResponse(
                    pk=pk,
                    question=GuildApplicationQuestion.objects.get(pk=question),
                    response=response,
                    application=GuildApplication.objects.get(pk=application)
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # CORE.GUILDAPPLICATIONTEMPLATE
        if line['model'] == 'core.guildapplicationtemplate' and 'core.guildapplicationtemplate' in enabled:
            try:
                pk=line['pk']
                questions=fields['questions']
                guild=fields['guild']
                app = GuildApplicationTemplate(
                    pk=pk,
                    guild=Guild.objects.get(pk=guild)
                )
                app.save()
                app.questions.set([GuildApplicationQuestion.objects.get(pk=x) for x in questions])
                app.save()
            except Exception as e:
                print(line)
                print(e)
        # DISCORD.DISCORDUSER
        if line['model'] == 'discord.discorduser' and 'discord.discorduser' in enabled:
            # TODO: groups
            pk=line['pk']
            user=users[fields['user']]
            username = fields['username']
            email = fields['email']
            refresh_token = fields['refresh_token']
            access_token = fields['access_token']
            external_id = fields['external_id']
            try:
                DiscordUser(
                    pk=pk,
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
            try:
                pk = line['pk']
                external_id = fields['external_id']
                group = fields['group']
                DiscordGroup(
                    pk=pk,
                    external_id=external_id,
                    group=Group.objects.get(pk=group),
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # DISCOURSE.DISCOURSEUSER
        if line['model'] == 'discourse.discourseuser' and 'discourse.discourseuser' in enabled:
            # TODO: groups
            try:
                pk = line['pk']
                external_id = line['pk']
                user=users[fields['user']]
                DiscourseUser(
                    pk=pk,
                    user=User.objects.get(username=user),
                    external_id=external_id
                ).save()
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(line)
                print(e)
        # DISCOURSE.DISCOURSEGROUP
        if line['model'] == 'discourse.discoursegroup' and 'discourse.discoursegroup' in enabled:
            try:
                pk = line['pk']
                external_id = fields['external_id']
                group = fields['group']
                DiscourseGroup(
                    pk=pk,
                    external_id=external_id,
                    group=Group.objects.get(pk=group)
                ).save()
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(line)
                print(e)
        # EVEONLINE.TOKEN
        if line['model'] == 'eveonline.token' and 'eveonline.token' in enabled:
            try:
                pk=line['pk']
                scopes=fields['scopes']
                access_token=fields['access_token']
                expires_in=fields['expires_in']
                refresh_token=fields['refresh_token']
                expiry=fields['expiry']
                EveToken(
                    pk=pk,
                    scopes=scopes,
                    access_token=access_token,
                    expires_in=expires_in,
                    refresh_token=refresh_token,
                    expiry=expiry,
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # CORPORATION
        if line['model'] == 'eveonline.evecorporation' and 'eveonline.evecorporation' in enabled:
            try:
                pk=line['pk']
                name=fields['name']
                member_count=fields['member_count']
                tax_rate=fields['tax_rate']
                ceo=None
                ticker=fields['ticker']
                alliance_id=fields['alliance_id']
                EveCorporation(
                    pk=pk,
                    name=name,
                    member_count=member_count,
                    tax_rate=tax_rate,
                    ceo=ceo,
                    ticker=ticker,
                    alliance_id=alliance_id
                ).save()
            except Exception as e:
                print(line)
                print(e)
        # EVEONLINE.EVECHARACTER
        if line['model'] == 'eveonline.evecharacter' and 'eveonline.evecharacter' in enabled:
            try:
                pk=line['pk']
                token = fields['token']
                character_name = fields['character_name']
                character_portrait = fields['character_portrait']
                try:
                    user = users[fields['user']]
                except:
                    pass
                corporation = fields['corporation']
                corporation_object = None
                if corporation:
                    corporation_object = EveCorporation.objects.get(pk=corporation)
                character_alt_type=fields['character_alt_type']
                character_id=fields['character_id']
                main=fields['main']
                EveCharacter(
                    pk=pk,
                    user=User.objects.get(username=user),
                    token=EveToken.objects.filter(pk=token).first(),
                    character_name=character_name,
                    corporation=corporation_object,
                    character_id=character_id,
                    character_alt_type=character_alt_type,
                    character_portrait=character_portrait
                ).save()
            except Exception as e:
                print(line)
                print(e)
                raise e
        # GROUP MIGRATION
        #if line['model'] == 'core.user' and 'group.migration' in enabled:
        #    user_groups = fields['groups']
        #    for group in user_groups:
        #        User.objects.get(username=fields['username']).groups.add(Group.objects.get(name=groups[group]))
        # DISCORD GROUP MIGRATION
        #if line['model'] == 'discord.discorduser' and 'discord.group.migration' in enabled:
        #    user_groups = fields['groups']
        #    for group in user_groups:
        #        DiscordUser.objects.get(user=User.objects.get(username=users[fields['user']])).groups.add(DiscordGroup.objects.get(external_id=group))
        # DISCOURSE GROUP MIGRATION
        #if line['model'] == 'discourse.discourseuser' and 'discourse.group.migration' in enabled:
        #    user_groups = fields['groups']
        #    for group in user_groups:
        #        DiscourseUser.objects.get(user=User.objects.get(username=users[fields['core.user']])).groups.add(DiscourseGroup.objects.get(external_id=group))
        # PASSWORD MIGRATION
        if line['model'] == 'core.user' and 'password.filler' in enabled:
            try:
                password = line['fields']['password']
                username = line['fields']['username']
                user = User.objects.get(username=username)
                user.password = password
                user.save()
            except Exception as e:
                print(line)
                print(e)
    # GUILD MIGRATION
    if 'guild.migration' in enabled:
        for guild in Guild.objects.all():
            for user in User.objects.all():
                if guild.group in user.groups.all():
                    user.guilds.add(guild)
