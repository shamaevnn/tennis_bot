release: python manage.py test && python manage.py migrate --noinput
web: uvicorn tennis_bot.asgi:application --host 0.0.0.0 --port 8000
worker: celery -A tennis_bot worker --loglevel=INFO
beat: celery -A tennis_bot beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
