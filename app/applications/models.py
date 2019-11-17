from django.db import models
from django.contrib.auth.models import User, Group 

class ApplicationTemplate(models.Model):
    name = models.CharField(max_length=64) # display name 
    description = models.TextField()
    questions = models.ManyToManyField("ApplicationQuestion", blank=True)
    groups_to_add = models.ManyToManyField(Group, blank=True, related_name="groups_to_add") # groups to add on APPROVAL
    groups_to_remove = models.ManyToManyField(Group, blank=True, related_name="groups_to_remove") # groups to remove on APPROVE OR DENY
    required_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True) # optional required group

    def __str__(self):
        return self.name 

class ApplicationQuestion(models.Model):
    question_type_fields = (
        ("RESPONSE", "Response"),
        ("MODAL", "Modal")
    )

    name = models.CharField(max_length=256)
    help_text = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=16, choices=question_type_fields)

    # OPTIONAL: MODAL
    choices = models.CharField(max_length=256, blank=True, null=True) # comma delimited 

    def __str__(self):
        return self.name

class ApplicationResponse(models.Model):
    response = models.TextField()
    question = models.ForeignKey("ApplicationQuestion", on_delete=models.CASCADE)
    application = models.ForeignKey("Application", on_delete=models.CASCADE)

class Application(models.Model):
    application_status_fields = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected")
    )
    # BASIC INFORMATION
    status = models.CharField(max_length=16, choices=application_status_fields, default="PENDING")

    # USER
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_assigned", blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)

    # REFERENCES
    template = models.ForeignKey("ApplicationTemplate", on_delete=models.CASCADE)

    def __str__(self):
        return self.request_user.username + "'s Application for " + self.template.name
    
    class Meta:
        unique_together = ('request_user', 'template')