"""
Must be ran via
python3 ../app/manage.py < setup.py
"""
from django.contrib.auth.models import Group
from django.conf import settings

for group in settings.GROUP_LIST:
    Group.objects.get_or_create(name=group)
