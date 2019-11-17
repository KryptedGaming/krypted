# Installation
For production installation, we use Docker. 

1. Grab our provided DevOps repository `git clone https://github.com/KryptedGaming/krypted-docker.git`
2. Modify the `.env` with your desired settings
3. Launch your production environment with `docker-compose up -d`
4. By default, you'll be on port 8000. You'll need to proxypass this on your host webserver. 

# The .env File
MYSQL_DATABASE=krypted
MYSQL_USER=krypted
MYSQL_PASSWORD=somepassword
MYSQL_HOST=db
REQUIREMENTS=KryptedGaming/django-eveonline-connector,KryptedGaming/django-eveonline-entity-extensions
EXTENSIONS=accounts,applications,django_eveonline_connector
|   Variable    |    Meaning   |
|  ---  |  ---  |
|   `MYSQL_DATABASE`    |   The database name you'd like to use    |
|   `MYSQL_USER`    |   The database user you'd like to use    |
|   `MYSQL_PASSWORD`    |   The database password you'd like to use    |
|   `REQUIREMENTS`    |   Packages to install. Obtain GitHub repositories in the format: <Username>/<Repository>    |
|   `EXTENSIONS`    |   Packages to enable.   |

