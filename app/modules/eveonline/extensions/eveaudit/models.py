from django.db import models
from django_mysql.models import JSONField
from modules.eveonline.models import EveCharacter

class EveCharacterData(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.SET_NULL, related_name="data", null=True)
    total_skillpoints = models.BigIntegerField(null=True)
    total_isk = models.FloatField(null=True)
    last_updated = models.DateField(auto_now=True)
    corporation_history = JSONField()
    clones = JSONField()
    contracts = JSONField()
    skill_tree = JSONField()
    skills = JSONField()
    journal = JSONField()
    contacts = JSONField()
    assets = JSONField()
    mails = JSONField()