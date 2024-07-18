from django.utils import timezone
from datetime import datetime
from django.db import models
from api.models.base_model import Base


def current_year():
    return datetime.now().year

class Device(Base):
    HDR = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField('Identificador', max_length=50, unique=True, db_index=True)
    report_map = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    software_version = models.CharField(max_length=50, blank=True, null=True)
    message_type = models.CharField(max_length=50, blank=True, null=True)
    data = models.CharField(max_length=50, blank=True, null=True)
    hora = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    speed_gps = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    satellites = models.CharField(max_length=50, blank=True, null=True)
    fix_status = models.CharField(max_length=50, blank=True, null=True)
    in_state = models.CharField(max_length=50, blank=True, null=True)
    out_state = models.CharField(max_length=50, blank=True, null=True)
    mode = models.CharField(max_length=50, blank=True, null=True)
    report_type = models.CharField(max_length=50, blank=True, null=True)
    message_number = models.CharField(max_length=50, blank=True, null=True)
    reserved = models.CharField(max_length=50, blank=True, null=True)
    assign_map = models.CharField(max_length=50, blank=True, null=True)
    power_voltage = models.FloatField(blank=True, null=True)
    bateria_suntech = models.FloatField(blank=True, null=True)
    connection_rat = models.CharField(max_length=50, blank=True, null=True)
    acceleration_x = models.FloatField(blank=True, null=True)
    acceleration_y = models.FloatField(blank=True, null=True)
    acceleration_z = models.FloatField(blank=True, null=True)
    ADC = models.CharField(max_length=50, blank=True, null=True)
    GPS_odometer = models.CharField(max_length=50, blank=True, null=True)
    trip_distance = models.CharField(max_length=50, blank=True, null=True)
    horimeter = models.CharField(max_length=100, default='0')
    trip_horimeter = models.CharField(max_length=50, blank=True, null=True)
    idle_time = models.CharField(max_length=50, blank=True, null=True)
    impact = models.FloatField(blank=True, null=True)
    SoC_battery_voltage = models.FloatField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    data_length = models.CharField(max_length=50, blank=True, null=True)
    RFID = models.CharField(max_length=50, blank=True, null=True)
    velocidade_instantanea = models.CharField(max_length=50, blank=True, null=True)
    velocidade_pico = models.CharField(max_length=50, blank=True, null=True)
    temperatura_instantanea = models.CharField(max_length=50, blank=True, null=True)
    temperatura_pico = models.CharField(max_length=50, blank=True, null=True)
    alert_id = models.CharField(max_length=50, blank=True, null=True)
    alert_modifier = models.CharField(max_length=50, blank=True, null=True)
    alert_data = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['horimeter']),
        ]
        verbose_name_plural = "Devices"

    def save(self, *args, **kwargs):
        try:
            # Convertendo para float e formatando com duas casas decimais
            self.horimeter = "{:.2f}".format(float(self.horimeter))
        except ValueError:
            self.horimeter = "0.00"  # Caso ocorra um ValueError
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device_id} - {self.model}"

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    log_message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now) 
    additional_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['device', 'timestamp']),
        ]
        verbose_name_plural = "Device Logs"

    def __str__(self):
        return f"{self.device.device_id} - {self.timestamp}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)