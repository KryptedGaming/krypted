# DJANGO IMPORTS
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
# MISC
import uuid

class UserInfo(models.Model):
    """
    Additional information attached to the User model.
    Reverse access using: info
    e.g user.info.region
    """
    # REFERENCE
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info")

    # DEMOGRAPHICS
    region = models.CharField(max_length=2, choices=settings.REGIONS)
    age = models.IntegerField(null=True)

    # PROFILE
    biography = models.TextField(blank=True, null=True)
    avatar = models.URLField(max_length=255, blank=True, null=True)

    # FUNCTIONALITY
    activation_key = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    secret = models.UUIDField(default=uuid.uuid4, editable=False)


    # PROPERTIES
    @property
    def discord(self):
        from modules.discord.models import DiscordUser
        return DiscordUser.objects.filter(user=self.user).first()

    @property
    def discourse(self):
        from modules.discourse.models import DiscourseUser
        return DiscourseUser.objects.filter(user=self.user).first()

    @property
    def eve_character(self):
        from modules.eveonline.models import EveCharacter
        return EveCharacter.objects.filter(user=self.user, main=None).first()

    @property
    def eve_characters(self):
        from modules.eveonline.models import EveCharacter
        return EveCharacter.objects.filter(user=self.user)

    def has_group_request(self, group):
        return GroupRequest.objects.filter(request_user=self.user, request_group=group, response_action="Pending").exists()

    def has_group(self, group):
        return group in self.groups.all()

    def get_tenure(self):
        import datetime, pytz
        tenure = datetime.datetime.now().replace(tzinfo=pytz.UTC) - self.date_joined
        tenure = tenure.total_seconds() / 60 / 60 / 24 / 365
        return tenure

    # FUNCTIONS
    def __str__(self):
        return self.user.username

class GroupInfo(models.Model):
    """
    Additional information attached to the Group object.
    Reverse access using: info
    e.g group.info.description
    """
    group_types = (
        ("PUBLIC", "PUBLIC"),
        ("PROTECTED", "PROTECTED"),
        ("PRIVATE", "PRIVATE")
    )

    # REFERENCES
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="info")

    # BASIC INFORMATION
    description = models.TextField()
    type = models.CharField(max_length=12, choices=group_types)

    # REFERENCES
    managers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.group.name

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
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groups_requested")
    request_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_requests")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      related_name="group_requests_processed")
    response_action = models.CharField(max_length=32, choices=response_action_fields)
    response_date = models.DateField(blank=True, null=True)

    class Meta:
        permissions = (
                ('manage_group_requests', u'Can manage group requests.'),
                ('audit_group_requests', u'Can view the group request audit log.')
        )
