# Docker Installation
For production installation, we use Docker. 

1. Grab our provided DevOps repository `git clone https://github.com/KryptedGaming/krypted-docker.git`
2. Modify the `.env` with your desired settings
3. Launch your production environment with `docker-compose up -d`
4. By default, you'll be on port 8000. You'll need to proxypass this on your host webserver. 

## .env variables

|   Variable    |    Meaning   |
|  ---  |  ---  |
|   `DJANGO_SECRET`    |   Django secret used for hashing. Keep safe. `https://miniwebtool.com/django-secret-key-generator/`  |
|   `VERSION`    |   Git branch to checkout. e.g `master`   |
|   `SITE_DOMAIN`    |   Site domain, e.g `https://localhost:8000`   |
|   `SITE_NAME`    |   Site name, e.g My Corporation   |
|   `MYSQL_DATABASE`    |   MYSQL Database name    |
|   `MYSQL_USER`    |   MYSQL Database user   |
|   `MYSQL_PASSWORD`    |   MYSQL Database password   |
|   `REQUIREMENTS`    |   Packages to install. Obtain GitHub repositories in the format: <Username>/<Repository>    |
|   `EXTENSIONS`    |   Packages to enable.   |


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