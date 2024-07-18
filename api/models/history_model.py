from django.contrib.auth.models import User
from django.db import models
from api.models.base_model import Base
from api.models.device_model import Device
from api.models.equipament_model import Equipament


class Report(Base):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    report_type = models.CharField(max_length=50, choices=[
        ('fuel_consumption', 'Fuel Consumption'),
        ('working_hours', 'Working Hours'),
        ('maintenance', 'Maintenance'),
        ('alerts', 'Alerts')
    ])
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return self.name

class HistoricalLog(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

class GraphData(Base):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    equipament = models.ForeignKey(Equipament, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=[
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months')
    ])
    data_type = models.CharField(max_length=50, choices=[
        ('fuel_consumption', 'Fuel Consumption'),
        ('working_hours', 'Working Hours'),
        ('maintenance', 'Maintenance'),
        ('alerts', 'Alerts')
    ])
    data = models.JSONField()

    def __str__(self):
        return f"{self.device.device_id} - {self.equipament.nome} - {self.period}"