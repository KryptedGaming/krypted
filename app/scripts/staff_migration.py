from core.models import *
import time
for user in User.objects.all():
    poweruser = Group.objects.get(name="POWERUSER")
    superuser = Group.objects.get(name="SUPERUSER")
    root = Group.objects.get(name="ROOT")
    staff_guild = Guild.objects.get(slug='admin')
    staff_group = staff_guild.group
    if poweruser in user.groups.all() or superuser in user.groups.all() or root in user.groups.all():
        print(user)
        user.groups.add(staff_group)
        user.guilds.add(staff_guild)
        time.sleep(1)
