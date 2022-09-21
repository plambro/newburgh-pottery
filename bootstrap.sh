#!/bin/bash

export PRINTERNAME=Star_TSP143__STR_T_001_

# Make any new migrations
echo "Making Migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000