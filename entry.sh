#!/bin/bash

# setting locale
locale-gen ko_KR.UTF-8
export LANG='ko_KR.UTF-8'
export LC_ALL='ko_KR.UTF-8'

python3 manage.py migrate                  # Apply database migrations
python3 manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start nginx processes
echo Starting nginx
cp ../possster.conf /etc/nginx/sites-available/possster.conf
ln -s /etc/nginx/sites-available/possster.conf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
service nginx start

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn possster.wsgi:application \
    --name possster \
    --bind unix:/srv/possster.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"
