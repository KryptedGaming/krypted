# Docker Administration
This will go over how to administrate your container. 

## Basic Docker
To get things like `<container_name>` or other variables we may mention here, you'll need to know some basic Docker. 

* `docker container ls` Lists all containers. You'll be able to get <container_name> from here. 
* `docker-compose up` Starts up your containers from a `docker-compose.yml`. Run with `-d` to detach from terminal.
* `docker-compose down` Stops your containers from a `docker-compose.yml`
* `docker-compose build` If you're using our `Dockerfile`, this will rebuild the image.
* `docker-compose pull` If you're using our image, this will update your images to the latest. 

## Creating Superuser Accounts
Superuser accounts have all Django permissions, and are optimal for your admin accounts. 

1. `docker container exec -it <container_name> python3 /opt/krypted/app/manage.py createsuperuser`
2. Fill out the information as required

## Running Django Commands
Some packages require you to run setup scripts or other Django commands.
1. `docker container exec -it <container_name> python3 /opt/krypted/app/manage.py <command>`

## Database Backups
Backups are important, you should do them frequently and every time before you updgrade. 
1. Create a backup with 
```
sudo docker-compose exec db sh -c 'exec mysqldump "$MYSQL_DATABASE" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" 2>/dev/null' | gzip > "`date +"%Y_%m_%d"`_krypted.sql.gz"
```
2. Restore a backup with 
```
zcat *krypted.tar.gz | docker-compose exec -T db sh -c 'exec mysql "$MYSQL_DATABASE" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD"'
```
