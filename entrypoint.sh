#!/bin/bash

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
