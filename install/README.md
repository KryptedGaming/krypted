# General
1. Run install_depdendencies.sh
2. Set up mod_wsgi // sudo apt-get install libapache2-mod-wsgi-py3
3. Run `install_ui.sh`, you may have to edit it depending on location
4. Copy application configs (`install_app_configs.sh`)
5. Fill out settings.py and other apps.py in enabled modules 

# Discourse
Discourse install is same as allianceauth https://allianceauth.readthedocs.io/en/v1.15.6/installation/services/discourse/

# Celery 
1. Install redis - https://www.rosehosting.com/blog/how-to-install-configure-and-use-redis-on-ubuntu-16-04/
2. Follow guide - https://medium.com/@yehandjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7

Tips
1. Update DNS // echo "nameserver 8.8.8.8" | sudo tee /etc/resolvconf/resolv.conf.d/base > /dev/null
2. Don't forget to add GroupRequest permissions to groups, otherwise they can't manage them
