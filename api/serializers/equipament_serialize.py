from rest_framework import serializers
from api.models.equipament_model import Equipament
from api.models.device_model import Device
from api.serializers.device_serializer import DeviceSerializer

class EquipamentReadSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    work_hour = serializers.SerializerMethodField()

    class Meta:
        model = Equipament
        fields = [
            'id', 'device', 'work_hour', 'initial_hour_machine', 'initial_hour_device', 'total_hour_meter',
            'name', 'year', 'model', 'measuring_point', 'fuel', 'pulse_number', 'tire_perimeter',
            'available_hours_per_month', 'average_consumption', 'speed_alert', 'temperature_alert',
            'shock_alert', 'effective_hours_odometer', 'odometer', 'notes', 'created_at', 'updated_at'
        ]

    def get_work_hour(self, obj):
        return obj.work_hour

class EquipamentWriteSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all(), required=False)

    class Meta:
        model = Equipament
        fields = [
            'id', 'device', 'initial_hour_machine', 'name', 'year', 'model', 'measuring_point', 'fuel',
            'pulse_number', 'tire_perimeter', 'available_hours_per_month', 'average_consumption',
            'speed_alert', 'temperature_alert', 'shock_alert', 'effective_hours_odometer', 'odometer', 'notes'
        ]

    def create(self, validated_data):
        device = validated_data.pop('device', None)
        if device:
            if Equipament.objects.filter(device=device).exists():
                raise serializers.ValidationError(f"Device with ID {device.device_id} is already associated with another Equipament.")
            validated_data['initial_hour_device'] = round(float(device.horimeter), 2)
        equipament = Equipament.objects.create(device=device, **validated_data)
        return equipament

    def update(self, instance, validated_data):
        device = validated_data.pop('device', None)
        if device and device != instance.device:
            if Equipament.objects.filter(device=device).exists():
                raise serializers.ValidationError(f"Device with ID {device.device_id} is already associated with another Equipament.")
            instance.device = device
            instance.initial_hour_device = round(float(device.horimeter), 2)
        
        for attr, value in validated_data.items():
            if attr not in ['initial_hour_device', 'work_hour', 'total_hour_meter']:
                setattr(instance, attr, value)
        
        instance.save()
        return instance
