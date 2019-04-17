web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2 --log-file -
worker: python manage.py runworker -v3 --traceback progress-worker
