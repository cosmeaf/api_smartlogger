# models.py

import uuid
from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.conf import settings

class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_%(class)ss'
    )
    history = HistoricalRecords()  # Histórico padrão

    objects = BaseManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, user=None):
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        abstract = True

# Defina o modelo principal
class MyModel(Base):
    name = models.CharField(max_length=255)

# Crie um modelo histórico separado, se necessário
class HistoricalMyModel(models.Model):
    # Inclua todos os campos que você deseja manter no histórico
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação')
    updated_at = models.DateTimeField('Última Atualização')
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)
    history_date = models.DateTimeField('Data do Histórico', auto_now_add=True)
    history_change_reason = models.CharField('Razão da Mudança', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Histórico do Meu Modelo'
        verbose_name_plural = 'Históricos dos Meus Modelos'
        ordering = ['-history_date']
