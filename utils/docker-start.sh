#!/usr/bin/env bash

cd /usr/src/app
python manage.py makemigrations arionBackend
python manage.py migrate
echo "Starting server"
python manage.py runserver 0.0.0.0:8000