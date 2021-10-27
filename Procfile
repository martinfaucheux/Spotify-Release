release: ./release.sh
web: gunicorn config.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery worker --app config.celery.app
scheduler: celery beat --app config.celery.app --scheduler django_celery_beat.schedulers:DatabaseScheduler