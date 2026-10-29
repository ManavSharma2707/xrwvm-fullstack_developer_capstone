#!/bin/bash
# Container start-up: prepare the database and static files, then serve.
set -e

echo "Applying database migrations"
python manage.py migrate --noinput

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port ${PORT:-8000}"
exec gunicorn --bind "0.0.0.0:${PORT:-8000}" --workers 2 djangoproj.wsgi
