from rest_framework import serializers
from api.models.maintenance_model import Maintenance
from core.config.get_logger import get_logger

logger = get_logger()

class MaintenanceSerializer(serializers.ModelSerializer):
    horas_uso_peca = serializers.SerializerMethodField()
    remaining_hours = serializers.ReadOnlyField()

    class Meta:
        model = Maintenance
        fields = [
            'id', 
            'equipament', 
            'name', 
            'os', 
            'usage_hours', 
            'alarm_hours', 
            'obs', 
            'remaining_hours', 
            'horas_uso_peca',
            'horimetro_inicial_suntech',
            'horimetro_inicial_maintenance'
        ]

    def get_horas_uso_peca(self, obj):
        horas_uso_peca = obj.horas_uso_peca
        logger.info(f"Renderizando horas_uso_peca: {horas_uso_peca}")
        return horas_uso_peca

    def create(self, validated_data):
        logger.info(f"Criando Maintenance com dados: {validated_data}")
        instance = super().create(validated_data)
        logger.info(f"Maintenance criado com dados: {instance.__dict__}")
        return instance

    def update(self, instance, validated_data):
        logger.info(f"Atualizando Maintenance com dados: {validated_data}")
        instance = super().update(instance, validated_data)
        logger.info(f"Maintenance atualizado com dados: {instance.__dict__}")
        return instance
