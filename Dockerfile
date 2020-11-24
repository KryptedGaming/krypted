# Docker file for building Django application of Krypted 
# Usage: docker build --build-arg VERSION=master ./docker/app/ 
FROM python:3.6

RUN apt-get update --no-install-recommends && \
    apt-get install --no-install-recommends -y \
    git \
    bzip2=1.0.6-9.2~deb10u1 \ 
    wget=1.20.1-1.1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2 && \ 
    wget https://github.com/ColorlibHQ/AdminLTE/archive/v3.0.5.tar.gz && \
    wget https://github.com/KryptedGaming/krypted/releases/download/v4.0.0/Accounts_v12.tar.gz

RUN adduser --disabled-password --gecos '' krypted

RUN mkdir -p /opt/krypted/app
COPY --chown=krypted:krypted app/ /opt/krypted/app/
COPY --chown=krypted:krypted conf/settings.py.example /opt/krypted/app/app/settings.py 
COPY --chown=krypted:krypted requirements.txt /opt/krypted/

RUN pip3 install -r /opt/krypted/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1 && \ 
    pip3 install uwsgi==2.0.18

RUN mkdir -p /opt/krypted/app/app/static && \ 
    mkdir -p /opt/krypted/app/accounts/static && \
    mkdir -p /opt/eveonline/static/ && \
    tar -xvf v3.0.5.tar.gz -C /opt/krypted/app/app/static/ > /dev/null && \
    tar -xvf Accounts_v12.tar.gz -C /opt/krypted/app/accounts/static/ > /dev/null && \
    bunzip2 /sqlite-latest.sqlite.bz2 && \ 
    cp /sqlite-latest.sqlite /opt/krypted/app/eveonline.sqlite && \
    mv /opt/krypted/app/app/static/AdminLTE-3.0.5 /opt/krypted/app/app/static/adminlte
    
# COPY ENTRYPOINT
COPY --chown=krypted:krypted conf/uwsgi.ini /opt/uwsgi.ini
COPY --chown=krypted:krypted scripts/app_entrypoint.sh /usr/local/bin/
COPY --chown=krypted:krypted scripts/dev_entrypoint.sh /usr/local/bin/
COPY --chown=krypted:krypted scripts/celery_entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

# CLEAN UP
RUN rm /*.tar.gz

ENTRYPOINT ["app_entrypoint.sh"]
