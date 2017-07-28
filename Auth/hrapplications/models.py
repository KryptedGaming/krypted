from django.db import models
from django.contrib.auth.models import User
from core.models import Guild
from eveonline.models import EveCharacter
# Create your models here.
class Application(models.Model):
    status_choices = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Rejected", "Rejected"),
        ("On Hold", "On Hold")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="application_user")
    questions = models.ManyToManyField("Question", related_name="application_questions")
    status = models.CharField(choices=status_choices, max_length=24, default="Processing")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(blank=True, null=True)

class Question(models.Model):
    title = models.CharField(max_length=254)
    help_text = models.CharField(max_length=254, blank=True, null=True)
    def __str__(self):
        return title

## GAME SPECIFIC HANDLING OF APPLICATIONS
class EveApplication(Application):
    main_character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE, related_name="main_character")
