FROM python:3.6

RUN apt-get update && \
    apt-get install -y \
    rabbitmq-server \
    supervisor

# COPY APPLICATION
COPY ./app /opt/app/
COPY ./install /opt/app/install/

# COPY CONFIGURATION FILES
COPY ./install/configuration/settings.py /opt/app/app/settings.py
COPY ./install/configuration/celery.py /opt/app/app/celery.py
COPY ./install/configuration/core.py /opt/app/core/apps.py
COPY ./install/supervisor.conf /etc/supervisor/conf.d/kryptedauth.conf

# COPY MODULE CONFIGURATION
COPY ./install/configuration/eveonline.py /opt/app/modules/eveonline/apps.py
COPY ./install/configuration/discord.py /opt/app/modules/discord/apps.py
COPY ./install/configuration/discourse.py /opt/app/modules/discourse/apps.py
COPY ./install/configuration/applications.py /opt/app/modules/applications/apps.py
COPY ./install/configuration/engagement.py /opt/app/modules/engagement/apps.py

# COPY EXTENSION CONFIGURATION
COPY ./install/configuration/eveonline_eveaudit.py /opt/app/modules/eveonline/extensions/eveaudit/apps.py
COPY ./install/configuration/eveonline_evedoctrine.py /opt/app/modules/eveonline/extensions/evedoctrine/apps.py

# COPY ENTRYPOINT
COPY ./install/entrypoint.sh /opt/app/entrypoint.sh
RUN chmod +x /opt/app/entrypoint.sh

# INSTALL PIP DEPENDENCIES
RUN pip3 install -r /opt/app/install/requirements.txt
RUN pip3 install uwsgi

# COPY AND INSTALL UI 
COPY ./install/ui.tar.gz /opt/app/install/ui.tar.gz
RUN python3 /opt/app/manage.py collectstatic
RUN tar -xzf /opt/app/install/ui.tar.gz -C /opt/app/static/global/

# EXPOSE PROD/DEV PORTS
EXPOSE 8000
EXPOSE 8050

# RUN uWSGI
# CMD ["uwsgi", "--ini", "/opt/app/install/uwsgi.ini"]
