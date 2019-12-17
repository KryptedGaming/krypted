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
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grouprequests_submitted")
    request_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_requests")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="grouprequests_managed")
    response_action = models.CharField(max_length=32, choices=response_action_fields, default="PENDING")
    response_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s's request to %s" % (self.request_user, self.request_group)

    class Meta:
        permissions = [
            ('bypass_group_requirement', "Can approve, reject, and view groups despite not being in them."),
        ]
        unique_together = ('request_user', 'request_group')

class OpenGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if ClosedGroup.objects.filter(group=self.group).exists():
            messages.add_message(request, messages.ERROR, 'Open Group was not saved. Group already exists as closed group.')
            return
        super(OpenGroup, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.group.name

class ClosedGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if OpenGroup.objects.filter(group=self.group).exists():
            messages.add_message(request, messages.ERROR, 'Closed Group was not saved. Group already exists as open group.')
            return
        super(ClosedGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.group.name