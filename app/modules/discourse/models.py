from django.db import models
from django.conf import settings
from core.models import User, Group, ModuleUser, ModuleGroup
from core.exceptions import RateLimitException
import requests, json, logging
logger = logging.getLogger(__name__)

# Create your models here.
class DiscourseUser(ModuleUser):
    # REFERENCES
    groups = models.ManyToManyField('DiscourseGroup')

    def add_group(self, discourse_group):
        pass

    def remove_group(self, discourse_group):
        pass

    def __str__(self):
        return self.user.username

class DiscourseGroup(ModuleGroup):
    def get_users():
        pass
