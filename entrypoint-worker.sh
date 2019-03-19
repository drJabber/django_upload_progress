#!/bin/bash

cd /app && python manage.py runworker -v3 --traceback progress-worker 
