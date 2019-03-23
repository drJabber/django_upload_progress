#!/bin/bash

#echo waiting for postgresql container start on 5432...;
#while ! nc -z db 5432;
#    do sleep 1;
#done;

python manage.py runworker -v3 --traceback progress-worker 
