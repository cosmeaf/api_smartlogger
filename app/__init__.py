from __future__ import absolute_import, unicode_literals

# Isso garantirá que a aplicação Celery seja sempre importada quando o Django iniciar
from .celery import app as celery_app

__all__ = ('celery_app',)