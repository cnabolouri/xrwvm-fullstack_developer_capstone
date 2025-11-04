#!/bin/sh
# entrypoint.sh — run migrations and start Gunicorn

echo "Running Django migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec "$@"
