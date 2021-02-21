from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import messages


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
    request_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grouprequests_submitted")
    request_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_requests")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="grouprequests_managed")
    response_action = models.CharField(
        max_length=32, choices=response_action_fields, default="PENDING")
    response_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s's request to %s" % (self.request_user, self.request_group)

    class Meta:
        permissions = [
            ('bypass_group_requirement',
             "Can approve, reject, and view groups despite not being in them."),
        ]


class ExtendedGroup(models.Model):
    extended_group_types = (
        ("OPEN", "OPEN"),
        ("REQUESTABLE", "REQUESTABLE"),
    )
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=extended_group_types)

    enabling_groups = models.ManyToManyField(
        Group, blank=True,
        help_text="Group(s) that allow the user access to the specified group.",
        related_name="enabler_for")

    def __str__(self):
        return self.group.name


class GroupTrigger(models.Model):
    trigger_group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name="trigger")
    target_groups = models.ManyToManyField(Group, blank=True)
    add_groups_on_trigger = models.BooleanField(
        default=False, help_text="When the trigger group is obtained, the user will obtain all target groups")
    remove_groups_on_trigger = models.BooleanField(
        default=False, help_text="When the trigger group is lost, the user will lose all target groups")

    def __str__(self):
        return f"Group Trigger: {self.trigger_group}"
