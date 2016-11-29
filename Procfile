web: gunicorn open_notices.wsgi --log-file -
worker: celery worker -A open_notices  --loglevel=info --concurrency=1