#!/bin/bash

docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml run django python manage.py migrate
docker-compose -f docker-compose.prod.yml up

