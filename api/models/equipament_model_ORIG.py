
from datetime import datetime
from django.db import models
from decimal import Decimal
from api.models.base_model import Base
from api.models.device_model import Device


def current_year():
    return datetime.now().year

class Equipament(Base):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='equipments')
    horimetro_inicialSuntech = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
    horimetro_inicialMaquina = models.FloatField('AZ Hora Máquina', default=0)
    horimetro_total = models.FloatField('Horímetro Total', default=0, editable=False)
    nome = models.CharField('Nome', max_length=255)
    ano = models.IntegerField('Ano', blank=True, null=True, default=current_year)
    numero_serie = models.CharField('Número de Série', max_length=255, unique=True)
    modelo = models.CharField('Modelo', max_length=255, default='N/A', blank=True, null=True)
    ponto_medicao = models.CharField('Ponto de Medição', max_length=255, default='N/A', blank=True, null=True)
    combustivel = models.CharField('Combustível', max_length=8, default='DIESEL', blank=True, null=True)
    numero_pulsos = models.IntegerField('Número de Pulsos', default=0, blank=True, null=True)
    perimetro_pneu = models.FloatField('Perímetro do Pneu (cm)', default=0.0, blank=True, null=True)
    horas_disponiveis_mes = models.FloatField('Horas Disponíveis por Mês', default=0.0, blank=True, null=True)
    consumo_medio = models.FloatField('Consumo Médio (m³/h - L/h - Kg/h)', default=0.0, blank=True, null=True)
    alerta_velocidade = models.FloatField('Alerta de Velocidade (km/h)', default=0.0, blank=True, null=True)
    alerta_temperatura = models.FloatField('Alerta de Temperatura (°C)', default=0.0, blank=True, null=True)
    alerta_shock = models.FloatField('Alerta de Shock (km/h)', default=0.0, blank=True, null=True)
    horas_efetivas_hodometro = models.CharField('Horas Efetivas ou Hodômetro', max_length=255, default='HODOMETRO', blank=True, null=True)
    hodometro = models.FloatField('Hodômetro', default=0.0, blank=True, null=True)
    obs = models.TextField('Observações', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device', 'nome']),
        ]
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return f"{self.nome} - {self.device}"

    @property
    def horas_trabalhadas(self):
        if self.device:
            hora_suntech = float(self.device.horimeter)
            horas_trabalhadas = hora_suntech + self.horimetro_inicialMaquina - self.horimetro_inicialSuntech
            return round(horas_trabalhadas, 2)
        return 0

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.device:
                self.horimetro_inicialSuntech = float(self.device.horimeter)
        super().save(*args, **kwargs)