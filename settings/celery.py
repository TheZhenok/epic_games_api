# Python
import os

# Third party
from celery import Celery
from celery.schedules import crontab

# Django
from django.conf import settings


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'settings.base'
)
app = Celery(
    'settings',
    broker=settings.CELERY_BROKER_URL
)
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)
app.autodiscover_tasks(
    lambda: settings.PROJECT_APPS
)
app.conf.beat_schedule = {
    'every-1-minute-every-day': {
        'task': 'games-price-updater',
        'schedule': crontab(
            minute='*/1'
        )
    }
}
app.conf.timezone = 'UTC'
