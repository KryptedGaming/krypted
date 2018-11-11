from core.models import *
import time
for user in User.objects.all():
    dnd_group = Group.objects.get(name="GAME-DND")
    dnd_new = Group.objects.get(name="DND")
    if dnd_group in user.groups.all():
        user.groups.add(dnd_new)
        time.sleep(1)
