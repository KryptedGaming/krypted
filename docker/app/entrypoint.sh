#!/bin/bash
export manage_py=/opt/krypted/app/manage.py

echo "Installing Python requirements supplied by environment"
IFS=',' read -ra REQUIREMENTS <<< "$REQUIREMENTS"
for REQUIREMENT in ${REQUIREMENTS[@]}; do
    IFS='/' read -ra REQUIREMENT <<< "$REQUIREMENT"
    if [ -z "${REQUIREMENT[1]}" ]; then 
        eval "pip3 install ${REQUIREMENT[0]} > /dev/null"
    else
        eval "git clone https://github.com/${REQUIREMENT[0]}/${REQUIREMENT[1]} /opt/${REQUIREMENT[1]} > /dev/null"
        eval "pip3 install -e /opt/${REQUIREMENT[1]} > /dev/null"
    fi 
done 
echo "Successfully installed Python requirements"

FORMATTED_EXTENSIONS=""
IFS=',' read -ra EXTENSIONS <<< "$EXTENSIONS"
for EXTENSION in ${EXTENSIONS[@]}; do
    FORMATTED_EXTENSIONS="$FORMATTED_EXTENSIONS '$(echo $EXTENSION | sed s/,//g)',"
done 

function replace_setting() {
    sed -i -E "s/$1/$2/g" /opt/krypted/app/app/settings.py
}

# set mysql settings 
echo "Replacing settings"
replace_setting "DJANGO_SECRET\s*=\s*'.*'" "DJANGO_SECRET= '${DJANGO_SECRET}'"
replace_setting "EXTENSIONS\s*=\s*\[.*\]" "EXTENSIONS = [${FORMATTED_EXTENSIONS}]"
echo "app.conf.broker_url = 'amqp://rabbitmq:5672'" >> /opt/krypted/app/app/celery.py

# install static files
mkdir -p /opt/krypted/app/app/static 
mkdir -p /opt/krypted/app/accounts/static

echo "Unpacking UI files"
tar -xvf AdminLTE-2.4.15.tar.gz -C /opt/krypted/app/app/static/ > /dev/null
tar -xvf Accounts_v12.tar.gz -C /opt/krypted/app/accounts/static/ > /dev/null

# finalize project
python3 /opt/krypted/app/manage.py makemigrations
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
        $directory/install.sh
    fi 
done 

uwsgi --check-static /var/html/krypted --check-static /opt/krypted/app --ini /opt/uwsgi.ini --uid krypted 