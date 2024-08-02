from decimal import Decimal
import logging
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from api.models.base_model import Base
from core.config.get_logger import get_logger

logger = get_logger()

def current_year():
    return datetime.now().year

class Equipament(Base):
    device = models.OneToOneField('Device', on_delete=models.CASCADE, related_name='equipments')
    begin_hour_device = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
    begin_hour_machine = models.FloatField('AZ Hora Máquina', default=0)
    total_hour_meter = models.FloatField('Horímetro Total', default=0, editable=False)
    name = models.CharField('Nome', max_length=255)
    year = models.IntegerField('Ano', blank=True, null=True, default=current_year)
    model = models.CharField('Modelo', max_length=255, default='N/A', blank=True, null=True)
    measuring_point = models.CharField('Ponto de Medição', max_length=255, default='N/A', blank=True, null=True)
    fuel = models.CharField('Combustível', max_length=8, default='DIESEL', blank=True, null=True)
    pulse_number = models.IntegerField('Número de Pulsos', default=0, blank=True, null=True)
    tire_perimeter = models.FloatField('Perímetro do Pneu (cm)', default=0.0, blank=True, null=True)
    available_hours_per_month = models.FloatField('Horas Disponíveis por Mês', default=0.0, blank=True, null=True)
    average_consumption = models.FloatField('Consumo Médio (m³/h - L/h - Kg/h)', default=0.0, blank=True, null=True)
    speed_alert = models.FloatField('Alerta de Velocidade (km/h)', default=0.0, blank=True, null=True)
    temperature_alert = models.FloatField('Alerta de Temperatura (°C)', default=0.0, blank=True, null=True)
    shock_alert = models.FloatField('Alerta de Shock (km/h)', default=0.0, blank=True, null=True)
    effective_hours_odometer = models.CharField('Horas Efetivas ou Hodômetro', max_length=255, default='HODOMETRO', blank=True, null=True)
    odometer = models.FloatField('Hodômetro', default=0.0, blank=True, null=True)
    notes = models.TextField('Observações', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device', 'name']),
        ]
        verbose_name_plural = "Equipamentos"
        verbose_name = "Equipamento"

    def __str__(self):
        return f"{self.name} - {self.device.device_id}"

    @property
    def work_hour(self):
        if self.device:
            hour_device = float(self.device.horimeter)
            work_hour = hour_device + self.begin_hour_machine - self.begin_hour_device
            return round(work_hour, 2)
        return 0

    def save(self, *args, **kwargs):
        if not self.pk:
            if Equipament.objects.filter(device=self.device).exists():
                raise ValidationError(f'O dispositivo {self.device.device_id} já está associado a outro equipamento.')
            if self.device:
                self.begin_hour_device = float(self.device.horimeter)
        self.total_hour_meter = self.work_hour
        super().save(*args, **kwargs)
