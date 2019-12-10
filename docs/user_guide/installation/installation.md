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


## Using Packages
Each package has their own installation settings. Refer to that package for special instructions. 