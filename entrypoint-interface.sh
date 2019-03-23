#!/bin/bash

#echo waiting for postgresql container start on 5432...;
#while ! nc -z db 5432;
#    do sleep 1 ;
#done;

exec daphne -b 0.0.0.0 -p 8000 config.asgi:application --verbosity 1