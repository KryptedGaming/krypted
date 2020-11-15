# Administration
These commands will assist you in administrating your Docker environment.

## Basic Docker Usage
* `docker-compose ls` Lists your containers.
* `docker-compose up` Starts up your containers from a `docker-compose.yml`. Run with `-d` to detach from terminal.
* `docker-compose down` Stops your containers from a `docker-compose.yml`
* `docker-compose build` If you're using our `Dockerfile`, this will rebuild the image.
* `docker-compose pull` If you're using our image, this will update your images to the latest. 

## Using Versions 
To ensure that your application will work as you'd expect, we recommend always specifying versions for:

1. Containers (e.g instead of `kryptedgaming/krypted:latest` use `kryptedgaming/krypted:X.Y.Z`)
2. Extensions (e.g instead of `django-eveonline-connector` use `django-eveonline-connector==X.Y.Z`)

This will save you a ton of grief later!


## Creating Superuser Accounts
Superuser accounts have all Django permissions, and are optimal for your admin accounts. 

* Run the command in the `app` container
```
docker-compose exec app python3 /opt/krypted/app/manage.py createsuperuser
```
* Fill out the information as required

## Database Backups
Backups are important, you should do them frequently and every time before you updgrade. 
### Creating Backups
```
sudo docker-compose exec db sh -c 'exec mysqldump "$MYSQL_DATABASE" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" 2>/dev/null' | gzip > "`date +"%Y_%m_%d"`_krypted.sql.gz"
```
### Restoring Backups
```
zcat *krypted.sql.gz | docker-compose exec -T db sh -c 'exec mysql "$MYSQL_DATABASE" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD"'
```