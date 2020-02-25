#!/bin/bash
export INSTALLED_APPS=accounts,group_requests,applications
pip install --upgrade pip
# install packages 
packages=$(ls -l app/packages/ | awk '{ print $9 }')
for package in $packages; do 
    pip3 install -e ./app/packages/"$package"
done 

# add to installed_apps
packages=$(find ./app/packages -name apps.py)
for package in $packages; do
    app=$(basename "$(dirname "$package")")
    export INSTALLED_APPS=$app,$INSTALLED_APPS
done 

python3 ./app/manage.py migrate 

# test packages 
for package in $packages; do 
    app=$(basename "$(dirname "$package")")
    echo "running tests for '$app'"
    if [ ! -z "$app" ]; then 
        python3 ./app/manage.py test "$app" --noinput --settings=app.settings
        if [ $? -ne 0 ]; then 
            exit 1
        fi
    fi 
done 

exit 0 