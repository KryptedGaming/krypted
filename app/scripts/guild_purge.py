from modules.discord.models import DiscordUser
from django.contrib.auth.models import User
from modules.guilds.models import Guild
from modules.discord.tasks import send_discord_message
import time
GUILD = "rust"
NAMES = "guild_purge.txt"

for line in open('scripts/guild_purge.txt'):
	name = line.split(",")[0]
	reason = line.split(",")[1]
	guild = Guild.objects.get(slug=GUILD)
	groups = guild.groups.all()
	user = User.objects.get(discord_user__username=name)
	for group in groups:
		if group in user.groups.all():
			user.groups.remove(group)
	guild.users.remove(user)
