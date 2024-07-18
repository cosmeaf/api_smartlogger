from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from core.config.get_logger import get_logger

logger = get_logger()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Configurações do broker
app.conf.update(
    broker_url='amqp://guest:guest@localhost:5672/',
    result_backend='rpc://',
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='America/Sao_Paulo',
)

@app.task(bind=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')
