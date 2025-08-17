#!/bin/sh

# Wait for the database to be ready
/usr/local/bin/python manage.py makemigrations
/usr/local/bin/python manage.py migrate

# Start the Django application
exec /usr/local/bin/python manage.py runserver 0.0.0.0:8000