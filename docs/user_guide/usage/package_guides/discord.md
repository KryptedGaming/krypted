# Discord Guide
## Quick Steps
To set up the `django_discord_connector` package:
1. Install it (varies, Docker vs Development)
2. (Recommended) Load the default schedule (`python3 manage.py loaddata discord_default_schedule`)
3. Create a Discord Application (https://discordapp.com/developers/applications)
4. Create a Discord client in the Admin Panel (`http://<your_site>/admin`)
5. Input the `CLIENT ID` from your Discord application 
6. Input the `CLIENT_SECRET` from your Discord application
7. Click `OAuth2` on your Discord application, set your `CALLBACK URL` (e.g `http://<your_site>/discord/sso/callback`)
8. Click `Bot` on your Discord application, set your `TOKEN`
9. Create a non-expiry Discord invite link, input it 
10. Invite your Bot to the Discord server (use the `OAuth2` bot tool)
11. Select your new client in the Admin Panel and click the dropdown, sync your groups

## Periodic Tasks
There are a ton of Discord tasks, below are the ones you need to worry about. 

| Command | Description |
| --- | --- |
| `sync_discord_user_groups`     | Update groups for Discord users (max 1 per second) |
| `sync_discord_users_accounts`     | Update nicknames and usernames for Discord users (max 1 per second) |
