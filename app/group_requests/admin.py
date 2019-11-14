from django.contrib import admin
from .models import ClosedGroup, OpenGroup

admin.site.register(ClosedGroup)
admin.site.register(OpenGroup)