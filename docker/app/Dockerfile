FROM python:3.6

RUN apt-get update && \
    apt-get install -y \
    git \
    bzip2 \ 
    wget 

RUN pip3 install uwsgi

RUN adduser --disabled-password --gecos '' krypted

ARG VERSION
RUN git clone --branch $VERSION https://github.com/KryptedGaming/krypted.git /opt/krypted/ && \
    cp /opt/krypted/install/settings_docker.py.example /opt/krypted/app/app/settings.py && \
    pip3 install -r /opt/krypted/install/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2

COPY uwsgi.ini /opt/
COPY supervisor.conf /etc/supervisor/

# EXPOSE PROD PORTS
EXPOSE 8000

# COPY ENTRYPOINT
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
