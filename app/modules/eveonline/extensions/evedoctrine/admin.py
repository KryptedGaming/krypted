from django.contrib import admin
from modules.eveonline.extensions.evedoctrine.models import EveFitting, EveDoctrine, EveSkillPlan

admin.site.register(EveDoctrine)
admin.site.register(EveFitting)
admin.site.register(EveSkillPlan)