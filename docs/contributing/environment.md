

# Development Environment
* [VSCode](https://code.visualstudio.com/) is our recommended IDE. We recommend the `Python` extension and `py-coverage-view`.
* Juniper Notebooks is highly recommended. Follow instructions from the `./launcher install` and use `python3 manage.py shell_plus --notebook`.
* Windows users are highly recommended to use [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

## Local Installation
Local installation is a safe bet for installation if you're unable to run Docker locally. Follow instructions [here](../installation/index.md#local-installation).

## Docker Installation
Docker is the preferred way to develop, as it will ensure that the entire stack is running. 

```
git clone https://github.com/KryptedGaming/krypted/
cd krypted/
cp conf/docker-compose.yml .
cp conf/.env . 
```

### Overview
For Docker Development, we'll be mounting local folders on the Docker image using `docker-compose.yml`. This will allow us to develop packages and immediately see their changes. 

### docker.compose.yml
Some changes are needed to your` docker-compose.yml` file, since we aren't interested in running production!

```
version: '2.0'

services:
    db:
        image: mysql:5.7
        volumes:
            - database:/var/lib/mysql
        restart: always
        command: --max_allowed_packet=256M
        environment:
            MYSQL_RANDOM_ROOT_PASSWORD: "yes"
            MYSQL_DATABASE: "${MYSQL_DATABASE}"
            MYSQL_USER: "${MYSQL_USER}"
            MYSQL_PASSWORD: "${MYSQL_PASSWORD}"

    redis:
        image: redis:6.0.9-alpine
        volumes:
            - "redis:/var/lib/redis"

    app:
        image: kryptedgaming/krypted:latest
        build: .
        env_file: .env
        entrypoint: dev_entrypoint.sh
        volumes:
            - "./app/packages/:/opt/krypted/app/packages"
        ports:
            - "8000:8000"
        depends_on:
            - db
    
    celery:
        image: kryptedgaming/krypted:latest
        restart: always
        build: .
        env_file: .env
        entrypoint: celery_entrypoint.sh
        volumes:
            - "./app/packages/:/opt/krypted/app/packages"
        depends_on:
            - db
            - app 

volumes:
    database: {}
    redis: {}
```

### Running
Edit `.env` and run the stack with the following commands.

```
sudo docker-compose build 
sudo docker-compose up -d 
```

If you change `.env`, you'll need to restart the stack. Otherwise, everything will dynamically reload. 