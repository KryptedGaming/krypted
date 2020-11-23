#!/bin/bash
export manage_py=/opt/krypted/app/manage.py

echo "Installing Python requirements supplied by environment"
IFS=',' read -ra PIP_INSTALLS <<< "$PIP_INSTALLS"
for PIP_INSTALL in ${PIP_INSTALLS[@]}; do
    eval "pip3 install ${PIP_INSTALL[0]}"
done 
IFS=',' read -ra GIT_INSTALLS <<< "$GIT_INSTALLS"
for GIT_INSTALL in ${GIT_INSTALLS[@]}; do
    IFS='/' read -ra GIT_INSTALL <<< "$GIT_INSTALL"
    eval "git clone https://github.com/${GIT_INSTALL[0]}/${GIT_INSTALL[1]} /opt/krypted/app/packages/${GIT_INSTALL[1]} > /dev/null"
done 
for LOCAL_PACKAGE in /opt/krypted/app/packages/* ; do 
    eval "pip3 install -e ${LOCAL_PACKAGE}"
done 
echo "Successfully installed Python requirements"

function replace_setting() {
    sed -i -E "s/$1/$2/g" /opt/krypted/app/app/settings.py
}

# finalize project
python3 /opt/krypted/app/manage.py migrate
python3 /opt/krypted/app/manage.py createcachetable > /dev/null
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
cd /opt/krypted/app/
python3 manage.py runserver 0.0.0.0:8000