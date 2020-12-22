# Django Discord Connector
1. Navigate to **Settings**
2. Click **Manage Settings** under `django_discord_connector`
3. Follow the steps below to obtain the values for each setting 

## Configuration
### Create a Discord Application 
1. Navigate to https://discordapp.com/developers/applications
2. Click “New Application”
3. Fill out a name, click create.
4. Add an application icon, description, and customize your application.
5. Copy the `CLIENT ID` value, save this for later.
6. Copy the `CLIENT SECRET` value, save this for later.

### Create a Bot
1. Click the Bot section
2. Add a Bot.
3. Customize your bot, add an icon and username.
4. Copy the `TOKEN` value, save this for later.

### Copy Server ID
1. Open your Discord settings
2. Navigate to Appearance
3. Enable Developer Mode
4. Right click your Server icon in the Discord menu
5. Copy ID. Save this for later.

### Create an Invite Link
1. Navigate to your server, hover over a channel and create an invite link.
2. Select no expiry, unlimited uses. Save this link for later.

## Usage
Typically, you'll just be mapping Discord Groups to standard Groups. 

### Pulling Discord Groups
Currently this is a bit clunky, a better interface is coming soon. 

1. Navigate to **Admin Panel**
2. Click **Periodic Tasks**
3. Create a task, name it "Pull Discord Groups"
4. Select the Task `django_discord_connector.sync_discord_groups`
5. Disable the task by default
6. Select an interval schedule 
7. Save 

Now, you'll be able to select that task and (from the Action dropdown) **Run selected task**. 

### Mapping Discord Groups
Once you've pulled your discord groups, you can attach them to standard Groups by going to **Discord Groups**, selecting the Discord Group you want to map, and selecting the standard Group. 

By default, Discord groups are applied every 5 minutes. You can edit this under **Periodic Tasks**, or manually run it. 