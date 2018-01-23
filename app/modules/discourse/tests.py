from django.test import TestCase
from django.contrib.auth.models import *
from modules.discourse.utils import *

# Create your tests here.
def addGroupTest():
    group = Group.objects.all()[0]
    addGroup(group)
