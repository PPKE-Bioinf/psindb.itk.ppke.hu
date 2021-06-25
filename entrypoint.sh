#!/bin/bash

#waiting for postgres
#until pg_isready --host=psindb-db --username=daniel
#do
#  echo "Waiting for PostgreSQL..."
#  sleep 1
#done

sleep 5
echo "DB is / should be ready..."

#python3 manage.py makemigrations consensx
#python3 manage.py migrate
#echo "Database migration complete."


# while true; do echo waiting; sleep 2; done

python3 manage.py migrate
echo "Database migration complete."
echo "Starting PSINDB..."
# python3 manage.py runserver 0.0.0.0:8000 --noreload
gunicorn --workers=4 --bind 0.0.0.0:8000 global_config.wsgi
