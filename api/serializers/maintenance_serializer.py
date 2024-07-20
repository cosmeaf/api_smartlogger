from rest_framework import serializers
from decimal import Decimal
from api.models.maintenance_model import Maintenance

class MaintenanceSerializer(serializers.ModelSerializer):
    remaining_hours = serializers.SerializerMethodField()
    horas_uso_peca = serializers.SerializerMethodField()

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
            'horas_uso_peca'
        ]

    def get_remaining_hours(self, obj):
        return obj.remaining_hours

    def get_horas_uso_peca(self, obj):
        return obj.horas_uso_peca

    def create(self, validated_data):
        equipament = validated_data.get('equipament')
        if equipament and equipament.device:
            validated_data['usage_hours'] = (
                Decimal(equipament.device.horimeter) 
                + Decimal(validated_data.get('horimetro_inicialMaintenance', 0)) 
                - Decimal(validated_data.get('horimetro_inicialSuntech', 0))
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        equipament = validated_data.get('equipament', instance.equipament)
        if equipament and equipament.device:
            validated_data['usage_hours'] = (
                Decimal(equipament.device.horimeter) 
                + Decimal(validated_data.get('horimetro_inicialMaintenance', instance.horimetro_inicialMaintenance)) 
                - Decimal(validated_data.get('horimetro_inicialSuntech', instance.horimetro_inicialSuntech))
            )
        return super().update(instance, validated_data)
