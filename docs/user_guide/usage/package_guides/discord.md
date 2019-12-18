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

## Detailed Steps
### 1. Create a Discord Application
1. Navigate to https://discordapp.com/developers/applications
2. Click "New Application"
3. Fill out a name, click create.
4. Add an application icon, description, and customize your application.
5. Copy the `CLIENT ID` value, save this for later. 
6. Copy the `CLIENT SECRET` value, save this for later. 

### 2. Get Bot Token 
1. Click the **Bot** section
2. Add a Bot.
3. Customize your bot, add an icon and username. 
4. Copy the `TOKEN` value, save this for later.

### 3. Inviting your Bot
1. Click the *OAuth2** section
2. Add a Redirect URL, `https://<your_domain>/discord/sso/callback` ((`your_site` is your site domain). Save this value for later.
3. Under the **Scopes** section, check the *bot* box. 
4. Scroll down to **Bot Permissions**, check *Administrator*.
5. Scroll back up to **Scopes**, copy the URL at the bottom and paste it in your browser.
6. Use this URL to invite the bot to your server. 

### 4. Get your Server ID 
1. Open your Discord settings
2. Navigate to Appearance
3. Enable Developer Mode
4. Right click your Server icon in the Discord menu
5. Copy ID. Save this for later. 

### 5. Create a permanant invite link 
1. Navigate to your server, hover over a channel and create an invite link.
2. Select no expiry, unlimited uses. Save this link for later. 

### 4. Creating the Discord Client
1. Navigate to your Admin Panel on the Krypted platform
2. Select Discord Clients
3. Create a new Discord client
4. Input the CALLBACK URL from Step #3 
5. Input the SERVER ID from Step #4 
6. Input the CLIENT ID from Step #1 
7. Input the CLIENT SECRET from Step #1 
8. Input the BOT TOKEN from Step #2
9. Input the INVITE LINK from Step #5 

## Recommened Task Schedule

| Command | Action | Interval |
| --- | --- | --- | 
| `django_discord_connector.tasks.verify_all_discord_users_groups`     | Verify groups | Every 5 minutes |
| `django_discord_connector.tasks.sync_discord_users_accounts`     | Update nicknames | Every week |
| `django_discord_connector.tasks.remote_sync_all_discord_users_groups`     | Verify groups with remote server | Every week | 