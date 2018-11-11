from core.models import *
import time
for user in User.objects.all():
    group = Group.objects.get(name="HR-MANAGER")
    hr = Group.objects.get(name="HR")
    if group in user.groups.all():
        user.groups.add(hr)
        time.sleep(1)
