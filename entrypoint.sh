#!/bin/sh
set -e

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# Apply database migrations (if needed)
# python manage.py migrate --noinput

# Start Gunicorn server
sh -c "cd ./playgroud_project && gunicorn playgroud_project.wsgi:application --bind 0.0.0.0:5000"
