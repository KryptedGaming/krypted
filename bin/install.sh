apt-get install python3 python3-pip mysql-server python-dev libmysqlclient-dev apache2 libapache2-mod-php5 libapache2-mod-wsgi
apt-get install screen unzip git redis-server curl libssl-dev libbz2-dev libffi-dev
pip3 install --upgrade pip
pip3 install -r requirements.txt
mkdir /var/log/auth
touch /var/log/auth/eveonline.log /var/log/auth/kryptedauth.log
chmod 777 /var/log/auth/eveonline.log /var/log/auth/kryptedauth.log
