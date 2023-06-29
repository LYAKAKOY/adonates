import os
from datetime import timedelta
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf.settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_payment_status': {
        'task': 'payments.tasks.check_payment_status',
        'schedule': timedelta(seconds=10),
    },
    'delete_canceled_payment': {
        'task': 'payments.tasks.delete_canceled_payment',
        'schedule': timedelta(hours=1),
    },
    'set_canceled_payment': {
        'task': 'payments.tasks.set_canceled_payment',
        'schedule': timedelta(seconds=10),
    },
}

app.conf.timezone = 'Europe/Moscow'
