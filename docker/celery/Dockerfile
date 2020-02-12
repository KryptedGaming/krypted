# Docker file for builing Celery application of Krypted 
# Usage: docker build --build-arg VERSION=master ./docker/celery/ 
FROM python:3.6
ARG VERSION

RUN apt-get update && \
    apt-get install -y \
    git \
    bzip2 \ 
    wget 

RUN adduser --disabled-password --gecos '' krypted

RUN git clone --branch $VERSION https://github.com/KryptedGaming/krypted.git /opt/krypted/ && \
    cp /opt/krypted/conf/settings.py.example /opt/krypted/app/app/settings.py && \
    pip3 install -r /opt/krypted/install/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1 && \ 
    pip3 install uwsgi 

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2

# COPY ENTRYPOINT
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
