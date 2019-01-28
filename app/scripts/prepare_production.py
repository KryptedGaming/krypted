from core.models import Group
for group in Group.objects.all():
    group.description = group.name
    group.save()
