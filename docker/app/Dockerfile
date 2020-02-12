# Docker file for building Django application of Krypted 
# Usage: docker build --build-arg VERSION=master ./docker/app/ 
FROM python:3.6
ARG VERSION

RUN apt-get update && \
    apt-get install -y \
    git \
    bzip2 \ 
    wget 

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2 && \ 
    wget https://github.com/KryptedGaming/krypted/releases/download/v4.0.0/AdminLTE-2.4.15.tar.gz && \
    wget https://github.com/KryptedGaming/krypted/releases/download/v4.0.0/Accounts_v12.tar.gz

RUN adduser --disabled-password --gecos '' krypted

RUN git clone --branch $VERSION https://github.com/KryptedGaming/krypted.git /opt/krypted/ && \
    cp /opt/krypted/conf/settings.py.example /opt/krypted/app/app/settings.py && \
    pip3 install -r /opt/krypted/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1 && \ 
    pip3 install uwsgi 

# COPY ENTRYPOINT
COPY uwsgi.ini /opt/uwsgi.ini
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
