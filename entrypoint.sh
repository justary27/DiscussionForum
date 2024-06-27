#!/bin/bash

echo "Applying db migrations"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

exec "$@"
