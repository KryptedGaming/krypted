# Installation
## Prerequisites 
1. Install Docker (`apt-get install docker docker-compose`)
2. Install Nginx or preferred webserver (`apt-get install nginx`)
3. Install Git (`apt-get install git`)
3. Clone the repository (`git clone https://github.com/KryptedGaming/kryptedauth.git`)

## Configuration
All files in `install/configuration` must be configured. 

### settings.py
1. Add a value for `SECRET_KEY`, use a [generator](https://www.miniwebtool.com/django-secret-key-generator/)
2. Add a value to `SERVER_DOMAIN` (e.g auth.kryptedgaming.com)
3. If you changed database values in the docker compose file, update `DATABASES`
4. Enable your desired modules in `INSTALLED_APPS` and `EXTENSIONS`
5. Add values for `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`

### eveonline.py
This is only required if you've enabled the `modules.eveonline`. 

1. Create a developer application [from the EVE Online website](https://developers.eveonline.com/applications)
2. Input the `ESI_CLIENT_ID`
3. Input the `ESI_SECRET_KEY`
4. Feel free to configure other values under USER SETTINGS

### discourse.py
This is only required if you've enabled `modules.discourse`

1. [Install Discourse(https://blog.discourse.org/2014/04/install-discourse-in-under-30-minutes/)
2. Input your forum URL into `DISCOURSE_BASE_URL`
3. Fill out `DISCOURSE_API_KEY` with your user API key
4. Fill out `DISCOURSE_API_USERNAME` with the username for the API key
5. Input `DISCOURSE_SSO_SECRET`
6. Enable SSO for Discourse

### discord.py
1. Input `SERVER_ID` by copying it with developer mode
2. Replace {code} in `DISCORD_INVITE_LINK`
3. Create a [Discord developer application](https://discordapp.com/developers/applications/)
4. Fill out values for `DISCORD_CLIENT_ID` and `DISCORD_SECRET`
5. Create a Discord bot, invite it, and fill out `DISCORD_BOT_TOKEN`

### celery.py
1. Update the `app.conf.beat_schedule` if you want

### core.py
1. [OPTIONAL] Input `GOOGLE_ANALYTICS_CODE` 
2. Input `SITE_TITLE`
3. Input `SITE_LOGO` (url format)
