# /api/models/maintenance_model.py 
from django.db import models
from decimal import Decimal
from api.models.base_model import Base
from api.models.equipament_model import Equipament

class Maintenance(Base):
    equipament = models.ForeignKey(Equipament, on_delete=models.CASCADE, related_name='maintenances')
    name = models.CharField(max_length=255)
    os = models.BooleanField(default=False)
    usage_hours = models.DecimalField(max_digits=10, decimal_places=2)
    alarm_hours = models.DecimalField(max_digits=10, decimal_places=2)
    obs = models.TextField(blank=True, null=True)

    @property
    def remaining_hours(self):
        return self.alarm_hours - self.usage_hours

    @property
    def horas_uso_peca(self):
        if self.equipament and self.equipament.device:
            horimetro_suntech = Decimal(self.equipament.device.horimeter)
            horimetro_inicial_peca = self.equipament.horimetro_inicialSuntech or Decimal(0)
            horas_uso_peca = self.usage_hours + (horimetro_suntech - horimetro_inicial_peca)
            return round(horas_uso_peca, 2)
        return Decimal(0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.equipament and self.equipament.device:
                self.usage_hours = Decimal(self.equipament.device.horimeter) - self.alarm_hours
        super().save(*args, **kwargs)

    def reset_usage_hours(self, additional_hours=0):
        if self.equipament and self.equipament.device:
            self.usage_hours = Decimal(self.equipament.device.horimeter) + Decimal(additional_hours)
            self.save()
