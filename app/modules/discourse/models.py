from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class DiscourseGroup(models.Model):
    role_id = models.CharField(max_length=255, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.group.name

class DiscourseUser(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField('DiscourseGroup')

    def __str__(self):
        return self.auth_user.username
