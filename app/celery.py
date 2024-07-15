from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configuração padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Usa uma string para não precisar serializar a configuração em objetos
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tarefas em aplicativos Django automaticamente
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')