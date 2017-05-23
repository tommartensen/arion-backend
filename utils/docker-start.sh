#!/usr/bin/env bash

cd /usr/src/app

echo "Set environment variables"
export SECRET_KEY=`date +%s | sha256sum | base64`
cat << EOF > arionBackend/local_settings.py
CORS_ORIGIN_WHITELIST = ["$HOST"]
SECRET_KEY = "$SECRET_KEY"
EOF

echo "Making migrations to database"
python manage.py makemigrations arionBackend
python manage.py migrate
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
