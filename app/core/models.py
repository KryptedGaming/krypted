from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup
from django.db import models
from django.conf import settings

"""
CORE MODELS
These are the core models of Krypted Authentication. They describe user interaction.
"""
class User(DjangoUser):
    """
    User model for Krypted Authentication.
    Extended off of the Django base user, with additional fields and properties.
    """
    # BASIC FIELDS
    avatar = models.URLField(max_length=255, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=2, choices=settings.REGIONS)

    # REFERENCES
    guilds = models.ManyToManyField("Guild", blank=True, null=True)

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
    guild = models.OneToOneField("Guild", on_delete=models.SET_NULL, blank=True, null=True)
    managers = models.ManyToManyField("User")

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
    date = models.DateField()
    password = models.CharField(max_length=5)
    value = models.DecimalField(max_digits=2)

    # REFERENCES
    user = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True)
    guild = models.ForeignKey("Guild", on_delete=models.SET_NULL, blank=True, null=True)

class Guild(models.Model):
    """
    Guild model for Krypted Authentication. Guilds are used to describe a particular set of players.
    """
    # BASIC INFORMATION
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=8)
    date_formed = models.DateField(auto_now=True)

    # REFERENCES
    group = models.OneToOneField("Group", on_delete=models.SET_NULL)

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
        "PENDING", "Pending",
        "ACCEPTED", "Accepted",
        "REJECTED", "Rejected",
        "RETRACTED", "Retracted"
    )
    # AUTHENTICATION
    request_user = models.ForeignKey("User", on_delete=models.CASCADE)
    request_group = models.OneToOneField("Group", on_delete=models.CASCADE)
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey("User", on_delete=models.SET_NULL)
    response_action = models.CharField(max_length=32, choices=response_action_fields)
    response_date = models.DateField(blank=True, null=True)

class GuildApplicationTemplate(models.Model):
    """
    Guild Application Template for Krypted Authentication
    Used to build Guild applications, which can be filled out by users and recorded as GuildApplication() objects
    """
    # REFERENCES
    guild = models.OneToOneField("Guild", on_delete=models.CASCADE)
    questions = models.ManyToManyField("GuildApplicationQuestion")


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
    name = models.CharField(max_length=32)
    help_text = models.TextField()
    type = models.CharField(max_length=16, choices=question_type_fields)

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
    request_user = models.ForeignKey("User", on_delete=models.CASCADE)
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey("User", on_delete=models.CASCADE)
    response_date = models.DateField(blank=True, null=True)

"""
ABSTRACT MODELS
These are abstract models, extended by other modules of the application
"""
class ModuleUser(models.Model):
    """
    User for third-party modules like Discourse, Discord, and Slack
    """
    external_id = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE)

    class Meta:
        abstract=True

class ModuleGroup(models.Model):
    """
    Group for third-party modules like Discourse, Discord, and Slack
    """
    external_id = models.IntegerField(blank=True, null=True)
    group = models.OneToOneField("Group", on_delete=models.CASCADE)

    class Meta:
        abstract=True
