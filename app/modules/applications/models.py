from django.db import models
from django.contrib.auth.models import User, Group

class ApplicationTemplate(models.Model):
    """
    Application Template for Krypted Authentication
    Used to build applications, which can be filled out by users and recorded as Application() objects
    """
    # REFERENCES
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="application_template")
    questions = models.ManyToManyField("ApplicationQuestion", blank=True)
    automated = models.BooleanField(default=True)

    def __str__(self):
        return self.group.name


class ApplicationQuestion(models.Model):
    """
    Application Question for Krypted Authentication
    Used to be filled out by users in Application() objects, recorded as ApplicationResponse() objects
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

class ApplicationResponse(models.Model):
    # BASIC INFORMATION
    response = models.TextField()
    # REFERENCES
    question = models.ForeignKey("ApplicationQuestion", on_delete=models.CASCADE)
    application = models.ForeignKey("Application", on_delete=models.CASCADE)

class Application(models.Model):
    application_status_fields = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected")
    )
    # BASIC INFORMATION
    status = models.CharField(max_length=16, choices=application_status_fields)

    # USER
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    request_date = models.DateField(auto_now=True)

    # MANAGEMENT
    response_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_assigned", blank=True, null=True)
    response_date = models.DateField(blank=True, null=True)

    # REFERENCES
    template = models.ForeignKey("ApplicationTemplate", on_delete=models.CASCADE)

    def __str__(self):
        return self.request_user.username + "'s Application to " + self.template.group.name
