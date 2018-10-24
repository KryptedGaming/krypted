from django.test import TestCase
from core.models import User, Group

# Create your tests here.
def mass_add_test():
    for user in User.objects.all():
        user.groups.add(Group.objects.all()[0])
        user.groups.add(Group.objects.all()[1])

def mass_remove_test():
    for user in User.objects.all():
        user.groups.remove(Group.objects.all()[0])
        user.groups.remove(Group.objects.all()[1])
