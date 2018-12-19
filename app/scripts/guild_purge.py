from modules.discord.models import DiscordUser
from core.models import User, Guild, Group
from modules.discord.tasks import send_discord_message
import time
GUILD = "rust"
NAMES = "guild_purge.txt"

for line in open('scripts/guild_purge.txt'):
    name = line.split(",")[0]
    reason = line.split(",")[1]
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
        "You have been purged from %s for reason: %s. Please contact guild staff if you have questions, feedback, or issues." % (guild.name, reason.strip()),
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
