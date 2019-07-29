#!/bin/bash
echo "Installing the Krypted Platform developer environment"
if [ ! -d "./app" ]; then
    echo "Please run in the root project directory"
    exit 1
fi

# Install python requirements
echo "Installing Python Requirements"
pip3 install -r ./install/requirements.txt

# Set up the Django project
echo "Setting up the Django Project"
python3 ./app/manage.py makemigrations
python3 ./app/manage.py migrate 
python3 ./app/manage.py collectstatic

# Create STATIC directory
mkdir -p ./app/app/static

# Install AdminLTE UI
echo "Installing AdminLTE in app/static/adminlte/"
tar -xvf install/AdminLTE-2.4.15.tar.gz -C ./app/app/static/

# Install AccountStylingV2
echo "Installing Accounts Styling in app/static/accounts"
tar -xvf install/Accounts-2.tar.gz -C ./app/app/static/