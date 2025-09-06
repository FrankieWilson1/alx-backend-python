#!/bin/sh
set -e

# Wait for the database to be ready
echo "waiting for the database to be ready..."
until nc -z db 3306; do
    echo "Database is unavailable - Sleeping..."
    sleep 1
done

echo "Database is ready. Starting migrations."

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
echo "Starting Django server."
python manage.py runserver 0.0.0.0:8000
