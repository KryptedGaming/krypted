from django.test import TestCase
from django.contrib.auth.models import User,Group
import time

# Create your tests here.
def discord_test():
    user = User.objects.all()[0]
    groups = Group.objects.all()
    for group in groups:
        user.groups.add(group)

def discord_kill():
    user = User.objects.all()[0]
    for group in User.objects.all()[0].groups.all():
        user.groups.remove(group)
