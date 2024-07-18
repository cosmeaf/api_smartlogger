from rest_framework import serializers
from decimal import Decimal
from api.models.maintenance_model import Maintenance

class MaintenanceSerializer(serializers.ModelSerializer):
    remaining_hours = serializers.SerializerMethodField()
    horas_uso_peca = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = ['id', 'equipament', 'name', 'os', 'usage_hours', 'alarm_hours', 'obs', 'remaining_hours', 'horas_uso_peca']

    def get_remaining_hours(self, obj):
        return obj.remaining_hours

    def get_horas_uso_peca(self, obj):
        return obj.horas_uso_peca

    def create(self, validated_data):
        equipament = validated_data.get('equipament')
        validated_data['usage_hours'] = Decimal(equipament.device.horimeter) - validated_data['alarm_hours']
        return super().create(validated_data)
