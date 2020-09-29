#!/bin/bash
export manage_py=/opt/krypted/app/manage.py

echo "Installing Python requirements supplied by environment"
IFS=',' read -ra PIP_INSTALLS <<< "$PIP_INSTALLS"
for PIP_INSTALL in ${PIP_INSTALLS[@]}; do
    eval "pip3 install ${PIP_INSTALL[0]} > /dev/null"
done 
IFS=',' read -ra GIT_INSTALLS <<< "$GIT_INSTALLS"
for GIT_INSTALL in ${GIT_INSTALLS[@]}; do
    IFS='/' read -ra GIT_INSTALL <<< "$GIT_INSTALL"
    eval "git clone https://github.com/${GIT_INSTALL[0]}/${GIT_INSTALL[1]} /opt/${GIT_INSTALL[1]} > /dev/null"
    eval "pip3 install -e /opt/${GIT_INSTALL[1]} > /dev/null"
done 
echo "Successfully installed Python requirements"

function replace_setting() {
    sed -i -E "s/$1/$2/g" /opt/krypted/app/app/settings.py
}

# set mysql settings 
echo "Replacing settings"
echo "app.conf.broker_url = 'amqp://rabbitmq:5672'" >> /opt/krypted/app/app/celery.py

# finalize project
python3 /opt/krypted/app/manage.py migrate
python3 /opt/krypted/app/manage.py createcachetable
python3 /opt/krypted/app/manage.py loaddata celery_interval_schedule
echo "Collecting static files"
cat <(echo "yes") - | python3 /opt/krypted/app/manage.py collectstatic > /dev/null
echo "Static files successfully collected"

# run conditional scripts 
for directory in /opt/*/; do 
    if [ -f "$directory/install.sh" ]; then 
        echo "Running conditional script: $directory/install.sh"
        "$directory/install.sh"
    fi 
done 

uwsgi --check-static /var/html/krypted --check-static /opt/krypted/app --ini /opt/uwsgi.ini --uid krypted 