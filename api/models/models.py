# import uuid
# from datetime import datetime
# from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from api.models.base_model import Base
from api.models.device_model import Device
from api.models.equipament_model import Equipament

# def current_year():
#     return datetime.now().year

# class Base(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
#     updated_at = models.DateTimeField('Última Atualização', auto_now=True)
#     deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

#     class Meta:
#         abstract = True

# class Device(Base):
#     HDR = models.CharField(max_length=50, blank=True, null=True)
#     device_id = models.CharField('Identificador', max_length=50, unique=True, db_index=True)
#     report_map = models.CharField(max_length=50, blank=True, null=True)
#     model = models.CharField(max_length=50, blank=True, null=True)
#     software_version = models.CharField(max_length=50, blank=True, null=True)
#     message_type = models.CharField(max_length=50, blank=True, null=True)
#     data = models.CharField(max_length=50, blank=True, null=True)
#     hora = models.CharField(max_length=50, blank=True, null=True)
#     latitude = models.CharField(max_length=50, blank=True, null=True)
#     longitude = models.CharField(max_length=50, blank=True, null=True)
#     speed_gps = models.CharField(max_length=50, blank=True, null=True)
#     course = models.CharField(max_length=50, blank=True, null=True)
#     satellites = models.CharField(max_length=50, blank=True, null=True)
#     fix_status = models.CharField(max_length=50, blank=True, null=True)
#     in_state = models.CharField(max_length=50, blank=True, null=True)
#     out_state = models.CharField(max_length=50, blank=True, null=True)
#     mode = models.CharField(max_length=50, blank=True, null=True)
#     report_type = models.CharField(max_length=50, blank=True, null=True)
#     message_number = models.CharField(max_length=50, blank=True, null=True)
#     reserved = models.CharField(max_length=50, blank=True, null=True)
#     assign_map = models.CharField(max_length=50, blank=True, null=True)
#     power_voltage = models.FloatField(blank=True, null=True)
#     bateria_suntech = models.FloatField(blank=True, null=True)
#     connection_rat = models.CharField(max_length=50, blank=True, null=True)
#     acceleration_x = models.FloatField(blank=True, null=True)
#     acceleration_y = models.FloatField(blank=True, null=True)
#     acceleration_z = models.FloatField(blank=True, null=True)
#     ADC = models.CharField(max_length=50, blank=True, null=True)
#     GPS_odometer = models.CharField(max_length=50, blank=True, null=True)
#     trip_distance = models.CharField(max_length=50, blank=True, null=True)
#     horimeter = models.CharField(max_length=100, default='0')
#     trip_horimeter = models.CharField(max_length=50, blank=True, null=True)
#     idle_time = models.CharField(max_length=50, blank=True, null=True)
#     impact = models.FloatField(blank=True, null=True)
#     SoC_battery_voltage = models.FloatField(blank=True, null=True)
#     temperatura = models.FloatField(blank=True, null=True)
#     data_length = models.CharField(max_length=50, blank=True, null=True)
#     RFID = models.CharField(max_length=50, blank=True, null=True)
#     velocidade_instantanea = models.CharField(max_length=50, blank=True, null=True)
#     velocidade_pico = models.CharField(max_length=50, blank=True, null=True)
#     temperatura_instantanea = models.CharField(max_length=50, blank=True, null=True)
#     temperatura_pico = models.CharField(max_length=50, blank=True, null=True)
#     alert_id = models.CharField(max_length=50, blank=True, null=True)
#     alert_modifier = models.CharField(max_length=50, blank=True, null=True)
#     alert_data = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['device_id']),
#             models.Index(fields=['horimeter']),
#         ]
#         verbose_name_plural = "Devices"

#     def save(self, *args, **kwargs):
#         try:
#             self.horimeter = f"{float(self.horimeter) / 60:.2f}"
#         except ValueError:
#             self.horimeter = "0.00"
#         self.updated_at = timezone.now() 
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.device_id} - {self.model}"

# class DeviceLog(models.Model):
#     device = models.ForeignKey(Device, on_delete=models.CASCADE)
#     log_message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     additional_info = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['device', 'timestamp']),
#         ]
#         verbose_name_plural = "Device Logs"

#     def __str__(self):
#         return f"{self.device.device_id} - {self.timestamp}"


# class Equipament(Base):
#     device = models.OneToOneField(Device, on_delete=models.PROTECT, related_name='equipments')
#     horimetro_inicialSuntech = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
#     horimetro_inicialMaquina = models.FloatField('AZ Hora Máquina', default=0)
#     horimetro_total = models.FloatField('Horímetro Total', default=0, editable=False)
#     nome = models.CharField('Nome', max_length=255)
#     ano = models.IntegerField('Ano', blank=True, null=True, default=current_year)
#     numero_serie = models.CharField('Número de Série', max_length=255, unique=True)
#     modelo = models.CharField('Modelo', max_length=255, default='N/A', blank=True, null=True)
#     ponto_medicao = models.CharField('Ponto de Medição', max_length=255, default='N/A', blank=True, null=True)
#     combustivel = models.CharField('Combustível', max_length=8, default='DIESEL', blank=True, null=True)
#     numero_pulsos = models.IntegerField('Número de Pulsos', default=0, blank=True, null=True)
#     perimetro_pneu = models.FloatField('Perímetro do Pneu (cm)', default=0.0, blank=True, null=True)
#     horas_disponiveis_mes = models.FloatField('Horas Disponíveis por Mês', default=0.0, blank=True, null=True)
#     consumo_medio = models.FloatField('Consumo Médio (m³/h - L/h - Kg/h)', default=0.0, blank=True, null=True)
#     alerta_velocidade = models.FloatField('Alerta de Velocidade (km/h)', default=0.0, blank=True, null=True)
#     alerta_temperatura = models.FloatField('Alerta de Temperatura (°C)', default=0.0, blank=True, null=True)
#     alerta_shock = models.FloatField('Alerta de Shock (km/h)', default=0.0, blank=True, null=True)
#     horas_efetivas_hodometro = models.CharField('Horas Efetivas ou Hodômetro', max_length=255, default='HODOMETRO', blank=True, null=True)
#     hodometro = models.FloatField('Hodômetro', default=0.0, blank=True, null=True)
#     obs = models.TextField('Observações', null=True, blank=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['device', 'nome']),
#         ]
#         verbose_name_plural = "Equipamentos"

#     def __str__(self):
#         return f"{self.nome} - {self.device}"

#     @property
#     def horas_trabalhadas(self):
#         if self.device:
#             hora_suntech = float(self.device.horimeter)
#             horas_trabalhadas = hora_suntech + self.horimetro_inicialMaquina - self.horimetro_inicialSuntech
#             return round(horas_trabalhadas, 2)
#         return 0

#     def save(self, *args, **kwargs):
#         if self.pk is None:  # Novo equipamento
#             if self.device:
#                 self.horimetro_inicialSuntech = float(self.device.horimeter)
#         super().save(*args, **kwargs)



# Report Area
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
