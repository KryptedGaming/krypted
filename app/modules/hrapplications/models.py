from django.db import models
from django.contrib.auth.models import User
from core.models import Guild
from games.eveonline.models import EveCharacter

# Create your models here.
class ApplicationTemplate(models.Model):
    status_choices = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Rejected", "Rejected"),
        ("On Hold", "On Hold")
    )
    name = models.CharField(max_length=32)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name="guild")
    questions = models.ManyToManyField("Question", related_name="application_questions")
    def __str__(self):
        return self.name

class Application(models.Model):
    status_choices = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Rejected", "Rejected"),
        ("On Hold", "On Hold")
    )
    template = models.ForeignKey("ApplicationTemplate", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="application_user")
    status = models.CharField(choices=status_choices, max_length=24, default="Processing")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(blank=True, null=True)

class Question(models.Model):
    title = models.CharField(max_length=254)
    help_text = models.CharField(max_length=254, blank=True, null=True)
    def __str__(self):
        return self.title

class Response(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, blank=True, null=True)
    response = models.CharField(max_length=1200, blank=True, null=True)
    application = models.ForeignKey("Application", on_delete=models.CASCADE, related_name="response_applciation")

class Comment(models.Model):
    application = models.ForeignKey("Application", on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=254)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

