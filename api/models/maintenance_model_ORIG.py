from django.db import models
from decimal import Decimal
from api.models.base_model import Base
from api.models.equipament_model import Equipament
from core.config.get_logger import get_logger

logger = get_logger()

class Maintenance(Base):
    equipament = models.ForeignKey(Equipament, on_delete=models.CASCADE, related_name='maintenances')
    horimetro_inicial_suntech = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
    horimetro_inicial_maintenance = models.FloatField('AZ Hora Máquina', default=0)
    name = models.CharField(max_length=255)
    os = models.BooleanField(default=False)
    usage_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    alarm_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    obs = models.TextField(blank=True, null=True)

    @property
    def remaining_hours(self):
        remaining = self.alarm_hours - self.horas_uso_peca
        logger.info(f"Calculando remaining_hours: {self.alarm_hours} - {self.horas_uso_peca} = {remaining}")
        return remaining

    @property
    def horas_uso_peca(self):
        if self.equipament and self.equipament.device:
            hora_suntech = float(self.equipament.device.horimeter)
            horas_uso_peca = Decimal(self.usage_hours) + Decimal(hora_suntech) - Decimal(self.horimetro_inicial_maintenance)
            horas_uso_peca = round(horas_uso_peca, 2)
            logger.info(f"CALCULO HORAS USO DA PEÇA: {horas_uso_peca} = {self.usage_hours} + {hora_suntech} - {self.horimetro_inicial_maintenance:.2f}")
            return horas_uso_peca
        return Decimal(0)

    def save(self, *args, **kwargs):
        logger.info(f"Salvando Maintenance com dados: {self.__dict__}")
        if self.equipament and self.equipament.device:
            horimetro_atual = float(self.equipament.device.horimeter) if self.equipament.device.horimeter is not None else 0
            self.horimetro_inicial_suntech = horimetro_atual
            self.horimetro_inicial_maintenance = horimetro_atual
        super().save(*args, **kwargs)
        logger.info(f"Maintenance salvo com dados: {self.__dict__}")

    def reset_usage_hours(self):
        if self.equipament and self.equipament.device:
            self.usage_hours = Decimal(self.usage_hours) - Decimal(self.horas_uso_peca)
            self.usage_hours = round(self.usage_hours, 2)
            logger.info(f"Zerando o valor de horas de uso atualizando o usage hours: usage hours = {self.usage_hours}")
            self.save(update_fields=['usage_hours'])
    