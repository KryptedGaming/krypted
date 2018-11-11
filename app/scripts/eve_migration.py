import time
from core.models import User, Group, Guild
for user in User.objects.all():
    group = Group.objects.get(name="EVE-MAIN")
    if group in user.groups.all():
        user.guilds.add(Guild.objects.get(slug='eve'))
