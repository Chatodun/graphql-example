#!/bin/sh

set -o errexit

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput
python /app/manage.py create_user_permission

