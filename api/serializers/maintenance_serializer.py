from rest_framework import serializers
from api.models.maintenance_model import Maintenance
from core.config.get_logger import get_logger

logger = get_logger()

class MaintenanceSerializer(serializers.ModelSerializer):
    horas_uso_peca = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_hours = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

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
            'horimetro_inicial_suntech',
            'horimetro_inicial_maintenance',
            'horas_uso_peca',
            'remaining_hours'
        ]

    def create(self, validated_data):
        logger.info(f"Criando Maintenance com dados: {validated_data}")
        instance = super().create(validated_data)
        instance.save()
        logger.info(f"Maintenance criado com dados: {instance.__dict__}")
        return instance

    def update(self, instance, validated_data):
        logger.info(f"Atualizando Maintenance com dados: {validated_data}")
        instance = super().update(instance, validated_data)
        instance.save()
        logger.info(f"Maintenance atualizado com dados: {instance.__dict__}")
        return instance
