#!/bin/bash

apt-get update


apt-get install -y supervisor nginx python-dev python-pip python-virtualenv

mkdir /var/www/competition
cp -r ./ /var/www/competition
chown www-data:www-data /var/www/competition
virtualenv /var/www/competition/flask
/var/www/competition/flask/bin/pip install -r /var/www/competition/requirements.txt


cp /var/www/competition/nginx_conf /etc/nginx/sites-available/nginx_conf
ln -s /etc/nginx/sites-available/nginx_conf /etc/nginx/sites-enabled/nginx_conf
service nginx restart


cp /var/www/competition/gunicorn_flask.conf /etc/supervisor/conf.d/gunicorn_flask.conf
