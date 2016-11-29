web: gunicorn open_notices.wsgi --log-file -
worker: celery -A open_notices.tasks worker --loglevel=info --concurrency=1