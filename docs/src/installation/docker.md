# Docker Installation
For production installation, we use Docker. 

1. Grab our production-ready `docker-compose.yml` file (`wget https://raw.githubusercontent.com/KryptedGaming/krypted/development/conf/docker-compose.yml`)
2. Grab our example `.env` file (`wget https://raw.githubusercontent.com/KryptedGaming/krypted/development/conf/.env`)
3. Modify the `.env` with your desired settings
4. Launch your production environment with `docker-compose up -d`
5. By default, you'll be on port 8000. You'll need to proxypass this on your host webserver. 

## Environment Variables
Krypted supports numerous environment variables, which are set in your `.env` file.


### Required Environment Variables

|   Variable    |    Description   | Example | 
|  -  |  ---  | -- | 
| `DJANGO_SECRET`    |   [Django Secret](https://miniwebtool.com django-secret-key-generator/) used for hashing.  | `aosdfiajsdufihi234h9fasd` | 
| `VERSION`    |   Git branch to checkout. | `master` | 
| `DEBUG` | Enable Django debugging. | `True` or `False` | 
| `SITE_DOMAIN` | The domain of your site. | `auth.site.com` | 
| `SITE_TITLE` | The title of your site. | `My Site` | 
| `DATABASE` | Your database preference. | `SQLLITE` or `MYSQL` | 

### Optional Environment Variables

|   Variable    |    Description   | Example | 
|  -  |  ---  | -- | 
| `MYSQL_DATABASE`    |   MYSQL Database name    | `db` | 
| `MYSQL_USER`    |   MYSQL Database user   | `krypted` | 
| `MYSQL_PORT`    |   MYSQL Database port   | `3306` | 
| `MYSQL_PASSWORD`    |   MYSQL Database password   | `mypassword` | 
| `EMAIL_HOST` | Host for your SMTP server. **Enables email verification**. | `myemailserver.com` | 
| `EMAIL_PORT` | Port for your SMTP server. | `123` | 
| `EMAIL_HOST_USER` | User for your SMTP server. | `mail@krypted.com` | 
| `EMAIL_HOST_PASSWORD` | Password for your SMTP server. | `password` | 
| `EMAIL_USE_TLS` | You'll know if you need it. | `True` or `False` | 
| `DEFAULT_FROM_EMAIL` | You'll know if you need it. | None |
| `SITE_PROTOCOL` | Your transfer protocol. | `http://` or `https://`. 
| `INSTALLED_APPS` | Comma separated applications to add to `INSTALLED_APPS` | `django_discord_connector, django_eveonline_connector` | 
| `PIP_INSTALLS` | List of `pip` packages, comma separated. | `package1,package2,package3` | 
| `GIT_INSTALLS`| List of `pip` packages to install from GitHub, comma separated. <User>/<Repository>| `KryptedGaming/django-eveonline-connector,KryptedGaming/django-discord-connector` | 



## Example .env file
```
DJANGO_SECRET=secret
SITE_DOMAIN=localhost
SITE_TITLE=My Corporation
VERSION=development
MYSQL_DATABASE=krypted
MYSQL_USER=krypted
MYSQL_PASSWORD=somepassword
MYSQL_HOST=db
MYSQL_PORT=3306
REQUIREMENTS=KryptedGaming/django-discord-connector,KryptedGaming/django-eveonline-connector
EXTENSIONS=accounts,applications,group_requests,django_discord_connector,django_eveonline_connector
```

We'll pick this apart piece by piece.
1. We set the `DJANGO_SECRET` to `secret`, which isn't very secure, but it's something. All of our hashing will be done by this, so if we ever need to migrate we need this value. 
2. We set the `SITE_DOMAIN` to `localhost`, meaning users will access our website by going to `https://localhost`
3. We set the `SITE_NAME` to `My Corporation`, which will update certain areas of the site to have our name. 
4. `MYSQL_DATABASE` This is the database name that we'll use. 
5. `MYSQL_USER` This is the database user that has access to the above database. 
6. `MYSQL_PASSWORD` We obviously need the password. 
7. `MYSQL_HOST` Depending on where you're hosting your MYSQL database, you'll set this value. In this case, we're using docker-compose and our database is a local container on the same network. 
8. `MYSQL_PORT` You'll likely not need to change this. 
9. `REQUIREMENTS` Here's where the interesting part comes in. The REQUIREMENTS has two formats: `<Package Name>` and `<GitHub User>/<Repository Name>`. If we add something like `django_eveonline_connector`, pip will install it from the Python package index. If we specify `KryptedGaming/django-discord-connector`, we will grab it from GitHub. 
10. Requirements aren't enough because some repositories will have different names. We might have a better solution in the future, but for now you need to specify all of the `EXTENSIONS` to be added to `INSTALLED_APPS`. 

## Using Packages
Each package has their own installation settings. Refer to that package for special instructions. 