# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from core.config.get_logger import get_logger

logger = get_logger()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')
    logger.info(f'Broker URL: {self.app.conf.broker_url}')
    logger.info(f'Result Backend: {self.app.conf.result_backend}')
