from modules.discord.models import DiscordUser
from core.models import User, Guild, Group
from modules.discord.tasks import send_discord_message
import time
GUILD = "wow"
NAMES = "guild_purge.txt"

for name in open('scripts/guild_purge.txt'):
    guild = Guild.objects.get(slug=GUILD)
    groups = Group.objects.filter(guild=guild)
    try:
        print("Purging %s" % name)
        discord_user = DiscordUser.objects.get(username=name.strip())
        user = discord_user.user
        for group in groups:
            print("Removing %s" % group)
            user.groups.remove(group)
            time.sleep(2)
        user.guilds.remove(guild)
        send_discord_message(
        "#bot",
        "You have been purged from %s for reason: null. If this was a mistake, please contact the guild staff." % (guild.name),
        user=user.id
        )
        time.sleep(5)
    except:
        for group in groups:
            print("Removing %s" % group)
            user.groups.remove(group)
            time.sleep(2)
        user.guilds.remove(guild)
        print("Exception purging %s" % name)
