from django.db import models
from django.utils import timezone
from api.models.base_model import Base
from api.models.equipament_model import Equipament

class Maintenance(Base):
    equipament = models.ForeignKey(Equipament, on_delete=models.CASCADE, related_name='maintenances')
    name = models.CharField(max_length=255)
    os = models.BooleanField(default=False)
    usage_hours = models.FloatField()
    alarm_hours = models.FloatField()
    obs = models.TextField(blank=True, null=True)

    @property
    def remaining_hours(self):
        if self.equipament and self.equipament.device:
            horimeter = float(self.equipament.device.horimeter)
            remaining = self.alarm_hours - horimeter
            return remaining
        return 0

    @property
    def horas_trabalhadas(self):
        if self.equipament and self.equipament.device:
            hora_suntech = float(self.equipament.device.horimeter)
            horas_trabalhadas = hora_suntech + self.equipament.horimetro_inicialMaquina - self.equipament.horimetro_inicialSuntech
            return round(horas_trabalhadas, 2)
        return 0

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.equipament and self.equipament.device:
                self.usage_hours = float(self.equipament.device.horimeter) - self.alarm_hours
        super().save(*args, **kwargs)
