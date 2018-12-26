from django.contrib.auth.models import AbstractUser, Group as DjangoGroup, PermissionsMixin
from django.db import models
from django.conf import settings
from app.conf import groups as group_settings
import uuid, pytz, datetime

"""
CORE MODELS
These are the core models of Krypted Authentication. They describe user interaction.
"""
class User(AbstractUser):
    """
    User model for Krypted Authentication.
    Extended off of the Django base user, with additional fields and properties.
    """
    # BASIC FIELDS
    avatar = models.URLField(max_length=255, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=2, choices=settings.REGIONS)
    activation_key = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    age = models.IntegerField(null=True)

    # REFERENCES
    guilds = models.ManyToManyField("Guild", blank=True)
    groups = models.ManyToManyField("Group", blank=True)

    # PROPERTIES
    @property
    def discord(self):
        from modules.discord.models import DiscordUser
        return DiscordUser.objects.filter(user=self).first()

    @property
    def discourse(self):
        from modules.discourse.models import DiscourseUser
        return DiscourseUser.objects.filter(user=self).first()

    @property
    def eve_character(self):
        from games.eveonline.models import EveCharacter
        return EveCharacter.objects.filter(user=self, main=None).first()

    @property
    def eve_characters(self):
        from games.eveonline.models import EveCharacter
        return EveCharacter.objects.filter(user=self)

    def has_group_request(self, group):
        return GroupRequest.objects.filter(request_user=self, request_group=group, response_action="PENDING").exists()

    def has_group(self, group):
        return group in self.groups.all()

    def get_tenure(self):
        import datetime, pytz
        tenure = datetime.datetime.now().replace(tzinfo=pytz.UTC) - self.date_joined
        tenure = tenure.total_seconds() / 60 / 60 / 24 / 365
        return tenure

    # FUNCTIONS
    def in_staff_group(self):
        try:
            if Guild.objects.get(slug='admin').group in self.groups.all():
                return True
            else:
                return False
        except:
            return False

    def is_hr(self):
        try:
            if Group.objects.get(name=group_settings.HR_GROUP) in self.groups.all():
                return True
            else:
                return False
        except:
            return False

class Group(DjangoGroup):
    """
    Group model for Krypted Authentication.
    Extended off of the Django base group, with additional fields and propertiesself.
    Some notes:
        - null guild means community-wide group
    """
    group_types = (
        ("PUBLIC", "Public"),
        ("PROTECTED", "PROTECTED"),
        ("PRIVATE", "PRIVATE")
    )

    # BASIC INFORMATION
    description = models.TextField()
    type = models.CharField(max_length=12, choices=group_types)

    # REFERENCES
    guild = models.ForeignKey("Guild", on_delete=models.SET_NULL, blank=True, null=True, related_name="group_guild")
    managers = models.ManyToManyField("User", blank=True)

    # META
    class Meta:
        permissions = (
            ('manage_group_requests', u'Can manage group requests.'),
            ('audit_group_requests', u'Can audit group requests.'),
        )

class Event(models.Model):
    """
    Event model for Krypted Authentication
    This model is used to create community events that can be tracked for participation
    Some notes:
        - null guild means community-wide event
        - null user means needs to be assigned
    """

    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    description = models.TextField()
    start_datetime = models.DateTimeField(auto_now=False)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True)
    guild = models.ForeignKey("Guild", on_delete=models.SET_NULL, blank=True, null=True)

    # ATTENDENCE
    password = models.CharField(max_length=3)
    value = models.IntegerField(blank=True, null=True)
    registrants = models.ManyToManyField("User", blank=True, related_name="registrants")
    participants = models.ManyToManyField("User", blank=True, related_name="participants")

    @property
    def is_expired(self):
        time_delta = self.start_datetime - datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if time_delta.total_seconds() < 0:
            return True
        return False

    def get_absolute_url(self):
        return "/event/%s" % self.pk

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
                ('manage_events', u'Can manage events'),
        )


class Guild(models.Model):
    """
    Guild model for Krypted Authentication. Guilds are used to describe a particular set of players.
    """
    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=8)
    date_formed = models.DateField(auto_now=True)
    image = models.URLField()

    # REFERENCES
    group = models.OneToOneField("Group", on_delete=models.CASCADE, related_name="guild_group")


    def __str__(self):
        return self.name

"""
FUNCTIONAL MODELS
These are models used to achieve processes
"""
class GroupRequest(models.Model):
    """
    Group Request model for Krypted Authentication
    Used by users to create group requests, which require management approvement
    """
    response_action_fields = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("RETRACTED", "Retracted")
    )
    # AUTHENTICATION
    request_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="group_request_request_user")
    request_group = models.ForeignKey("Group", on_delete=models.CASCADE)
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    response_action = models.CharField(max_length=32, choices=response_action_fields)
    response_date = models.DateField(blank=True, null=True)

    class Meta:
        permissions = (
                ('manage_group_requests', u'Can manage group requests.'),
                ('audit_group_requests', u'Can view the group request audit log.')
        )

class GuildApplicationTemplate(models.Model):
    """
    Guild Application Template for Krypted Authentication
    Used to build Guild applications, which can be filled out by users and recorded as GuildApplication() objects
    """
    # REFERENCES
    guild = models.OneToOneField("Guild", on_delete=models.CASCADE)
    questions = models.ManyToManyField("GuildApplicationQuestion", blank=True)

    def __str__(self):
        return self.guild.name


class GuildApplicationQuestion(models.Model):
    """
    Guild Application Question for Krypted Authentication
    Used to be filled out by users in GuildApplication() objects, recorded as GuildApplicationResponse() objects
    """
    question_type_fields = (
        ("RESPONSE", "Response"),
        ("MODAL", "Modal")
    )
    # BASIC INFORMATION
    name = models.CharField(max_length=256)
    help_text = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=16, choices=question_type_fields)

    # OPTIONAL: MODAL
    choices = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

class GuildApplicationResponse(models.Model):
    # BASIC INFORMATION
    response = models.TextField()
    # REFERENCES
    question = models.ForeignKey("GuildApplicationQuestion", on_delete=models.CASCADE)
    application = models.ForeignKey("GuildApplication", on_delete=models.CASCADE)

class GuildApplication(models.Model):
    application_status_fields = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected")
    )
    # BASIC INFORMATION
    status = models.CharField(max_length=16, choices=application_status_fields)

    # USER
    request_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="guild_application_request_user")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="guild_application_response_user", blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)

    # REFERENCES
    template = models.ForeignKey("GuildApplicationTemplate", on_delete=models.CASCADE)

    def __str__(self):
        return self.request_user.username + "'s Application to " + self.template.guild.name

    class Meta:
        permissions = (
                ('manage_guild_applications', u'Can manage Guild applications'),
                ('audit_eve_applications', u'Can audit an EVE application'),
        )


"""
ABSTRACT MODELS
These are abstract models, extended by other modules of the application
"""
class ModuleUser(models.Model):
    """
    User for third-party modules like Discourse, Discord, and Slack
    """
    external_id = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField("core.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract=True

class ModuleGroup(models.Model):
    """
    Group for third-party modules like Discourse, Discord, and Slack
    """
    external_id = models.BigIntegerField(blank=True, null=True)
    group = models.OneToOneField("core.Group", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.group:
            return self.group.name
        else:
            return "None"

    class Meta:
        abstract=True
