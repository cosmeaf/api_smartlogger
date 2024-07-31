from decimal import Decimal
import logging
from datetime import datetime
from django.db import models
from api.models.base_model import Base
from core.config.get_logger import get_logger

logger = get_logger()

def current_year():
    return datetime.now().year

class Equipament(Base):
    device = models.OneToOneField('Device', on_delete=models.CASCADE, related_name='equipments')
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
        logger.info(f"Início do cálculo de horas trabalhadas para o equipamento {self.nome}.")
        
        if self.device:
            hora_suntech = float(self.device.horimeter)
            logger.info(f"Horímetro Suntech: {hora_suntech}")
            logger.info(f"Horímetro Inicial Máquina: {self.horimetro_inicialMaquina}")
            logger.info(f"Horímetro Inicial Suntech: {self.horimetro_inicialSuntech}")

            horas_trabalhadas = Decimal(hora_suntech) + Decimal(self.horimetro_inicialMaquina) - Decimal(self.horimetro_inicialSuntech)
            horas_trabalhadas = round(horas_trabalhadas, 2)

            logger.info(f"Resultado do cálculo de horas trabalhadas para o equipamento {self.nome}: {horas_trabalhadas}")
            return horas_trabalhadas
        
        logger.info(f"Equipamento {self.nome} não possui dispositivo associado. Horas trabalhadas são 0.")
        return Decimal(0)

    def save(self, *args, **kwargs):
        logger.info(f"Início do método save para o equipamento {self.nome}.")
        
        if self.pk is None and self.device:
            # Atualize o horímetro inicial com o valor do dispositivo
            self.horimetro_inicialSuntech = float(self.device.horimeter)
            logger.info(f"Definindo horímetro inicial Suntech para: {self.horimetro_inicialSuntech}")
        
        # Chama o método save da superclasse
        super().save(*args, **kwargs)
    
        logger.info(f"Equipamento {self.nome} salvo com sucesso.")


    def min_remaining_hours(self):
        from api.models.maintenance_model import Maintenance

        try:
            # Filtra as manutenções associadas ao equipamento
            maintenances = Maintenance.objects.filter(equipament=self)
            
            if maintenances.exists():
                # Encontra o menor valor de remaining_hours
                min_hours = min(
                    (Decimal(maintenance.remaining_hours) for maintenance in maintenances),
                    default=Decimal(0)  # Define 0 como valor padrão caso não haja registros
                )
                logger.info(f"Equipamento {self.nome}: Menor valor de remaining_hours encontrado: {min_hours}")
                return min_hours

            logger.info(f"Equipamento {self.nome}: Nenhum registro de manutenção encontrado.")
            return Decimal(0)

        except Exception as e:
            logger.error(f"Erro ao calcular min_remaining_hours para o equipamento {self.nome}: {e}")
            return Decimal(0)
