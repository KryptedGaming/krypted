from django.contrib import admin
from modules.applications.models import *

admin.site.register(ApplicationTemplate)
admin.site.register(ApplicationQuestion)
admin.site.register(ApplicationResponse)
admin.site.register(Application)
