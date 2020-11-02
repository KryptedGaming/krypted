# Docker file for building Django application of Krypted 
# Usage: docker build --build-arg VERSION=master ./docker/app/ 
FROM python:3.6
ARG VERSION

RUN apt-get update --no-install-recommends && \
    apt-get install --no-install-recommends -y \
    git \
    bzip2=1.0.6-9.2~deb10u1 \ 
    wget=1.20.1-1.1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2 && \ 
    wget https://github.com/KryptedGaming/krypted/releases/download/v4.0.0/AdminLTE-2.4.15.tar.gz && \
    wget https://github.com/KryptedGaming/krypted/releases/download/v4.0.0/Accounts_v12.tar.gz

RUN adduser --disabled-password --gecos '' krypted

RUN git clone --branch $VERSION https://github.com/KryptedGaming/krypted.git /opt/krypted/ && \
    cp /opt/krypted/conf/settings.py.example /opt/krypted/app/app/settings.py && \
    pip3 install -r /opt/krypted/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1 && \ 
    pip3 install uwsgi==2.0.18

RUN mkdir -p /opt/krypted/app/app/static && \ 
    mkdir -p /opt/krypted/app/accounts/static && \
    mkdir -p /opt/eveonline/static/ && \
    tar -xvf AdminLTE-2.4.15.tar.gz -C /opt/krypted/app/app/static/ > /dev/null && \
    tar -xvf Accounts_v12.tar.gz -C /opt/krypted/app/accounts/static/ > /dev/null && \
    cp /sqlite-latest.sqlite.bz2 /opt/eveonline/static/ && \
    bunzip2 /opt/eveonline/static/sqlite-latest.sqlite.bz2 && \ 
    rm sqlite-latest.sqlite.bz2

RUN chown -R krypted:krypted /opt/krypted

# COPY ENTRYPOINT
COPY uwsgi.ini /opt/uwsgi.ini
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
