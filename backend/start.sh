#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py collectstatic --noinput || true
gunicorn app.wsgi:application --bind 0.0.0.0:8000
