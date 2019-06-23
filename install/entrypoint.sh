#!/bin/sh
service rabbitmq-server start
service supervisor start
python3 /opt/app/manage.py makemigrations
python3 /opt/app/manage.py migrate
uwsgi --ini /opt/app/install/uwsgi.ini
