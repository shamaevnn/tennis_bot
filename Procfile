release: python manage.py migrate --noinput
web: gunicorn --bind :$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker tennis_bot.asgi:application
worker: celery -A tennis_bot worker --loglevel=INFO
beat: celery -A tennis_bot beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler