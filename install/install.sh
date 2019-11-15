#!/bin/bash
usage () {
    echo "Usage: $0 [dev]"
    echo "Commands:"
    echo "    dev:        Install development packages."
}

echo "Installing the Krypted Platform developer environment"
if [ ! -d "./app" ]; then
    echo "Please run in the root project directory"
    exit 1
fi

command=$1

if [ -n "$command" ]; then
    case "$command" in 
        dev)
        DEV_MODE=true
        ;;
        *)
        usage
        exit 1
        ;;
    esac
fi

# Install python requirements
echo "Installing Python Requirements"
pip3 install -r ./install/requirements.txt
if [ $? -ne 0 ]; then 
    echo "Failed to install Python requirements"
    exit 1
fi 
if [ $DEV_MODE ]; then
    echo "Installing Python Development Requirements"
    pip3 install -r ./install/requirements_dev.txt
    if [ $? -ne 0 ]; then 
        echo "Failed to install Python Development requirements"
        exit 1
    fi 
fi

# Set up the Django project
echo "Setting up the Django Project"
echo "Creating migrations for project"
python3 ./app/manage.py makemigrations
if [ $? -ne 0 ]; then 
    echo "Failed to set up the Django project"
    exit 1
fi 
echo "Creating migrations for specific subprojects"
python3 ./app/manage.py makemigrations accounts
if [ $? -ne 0 ]; then 
    echo "Failed to set up the Django project"
    exit 1
fi 
echo "Creating database for project"
python3 ./app/manage.py migrate 
if [ $? -ne 0 ]; then 
    echo "Failed to set up the Django project"
    exit 1
fi 

# Create STATIC directory
mkdir -p ./app/app/static
mkdir -p ./app/accounts/static

# Install AdminLTE UI
echo "Installing AdminLTE in app/static/adminlte/"
tar -xvf install/AdminLTE-2.4.15.tar.gz -C ./app/app/static/

# Install AccountStylingV2
echo "Installing Accounts Styling in app/static/accounts"
tar -xvf install/Accounts_v12.tar.gz -C ./app/accounts/static/

# Install Developer Settings
cp ./install/developer_settings.example ./app/app/settings.py

# Collect static
python3 ./app/manage.py collectstatic
