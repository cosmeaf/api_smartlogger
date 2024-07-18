
from rest_framework import serializers
from api.models.maintenance_model import Maintenance
from core.config.get_logger import get_logger

logger = get_logger()

class MaintenanceSerializer(serializers.ModelSerializer):
    remaining_hours = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = ['id', 'equipament', 'name', 'os', 'usage_hours', 'alarm_hours', 'obs', 'remaining_hours']

    def get_remaining_hours(self, obj):
        return round(obj.remaining_hours, 2)

    def create(self, validated_data):
        equipament = validated_data.get('equipament')
        validated_data['usage_hours'] = round(float(equipament.device.horimeter) - validated_data['alarm_hours'], 2)
        return super().create(validated_data)