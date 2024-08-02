import logging
from django.db import models
from decimal import Decimal
from api.models.base_model import Base
from core.config.get_logger import get_logger

logger = get_logger()

class Maintenance(Base):
    equipament = models.ForeignKey('Equipament', on_delete=models.CASCADE, related_name='maintenances')
    horimetro_inicial_suntech = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
    horimetro_inicial_maintenance = models.FloatField('AZ Hora Máquina', default=0)
    name = models.CharField(max_length=255)
    os = models.BooleanField(default=False)
    usage_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    alarm_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    obs = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['equipament']),
            models.Index(fields=['name']),
            models.Index(fields=['os']),
        ]
        verbose_name_plural = "Maintenance Records"
        verbose_name = "Maintenance Record"

    @property
    def remaining_hours(self):
        return self.alarm_hours - self.horas_uso_peca

    @property
    def horas_uso_peca(self):
        if self.equipament and self.equipament.device:
            hora_suntech = float(self.equipament.device.horimeter)
            horas_uso_peca = Decimal(self.usage_hours) + Decimal(hora_suntech) - Decimal(self.horimetro_inicial_maintenance)
            horas_uso_peca = max(horas_uso_peca, Decimal(0))  # Garante que o valor não seja negativo
            horas_uso_peca = round(horas_uso_peca, 2)
            return horas_uso_peca
        return Decimal(0)

    @property
    def background_color(self):
        if not self.os:
            color = ""
        else:
            remaining_hours = self.remaining_hours
            if remaining_hours >= 0:
                color = ""
            elif remaining_hours >= -50:
                color = "bg-yellow-300"  # Amarelo
            elif remaining_hours >= -100:
                color = "bg-orange-300"  # Laranja claro
            else:
                color = "bg-red-300"  # Vermelho

        logger.debug(f"OS status: {self.os}, Background color: {color}")
        return color

    def save(self, *args, **kwargs):
        if self.equipament and self.equipament.device:
            horimetro_atual = float(self.equipament.device.horimeter) if self.equipament.device.horimeter is not None else 0
            self.horimetro_inicial_suntech = horimetro_atual
            self.horimetro_inicial_maintenance = horimetro_atual
        super().save(*args, **kwargs)

    def reset_usage_hours(self):
        if self.equipament and self.equipament.device:
            self.usage_hours = Decimal(self.usage_hours) - Decimal(self.horas_uso_peca)
            self.usage_hours = round(self.usage_hours, 2)
            self.save(update_fields=['usage_hours'])
