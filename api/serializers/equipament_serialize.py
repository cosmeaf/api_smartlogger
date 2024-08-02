from rest_framework import serializers
from api.models.equipament_model import Equipament
from api.models.device_model import Device
from api.serializers.device_serializer import DeviceSerializer

class EquipamentSerializer(serializers.ModelSerializer):
    # Filtra apenas os dispositivos que não estão associados a nenhum Equipament
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.filter(equipments__isnull=True), required=False)
    work_hour = serializers.SerializerMethodField()

    class Meta:
        model = Equipament
        fields = [
            'id', 'device', 'work_hour', 'begin_hour_machine', 'begin_hour_device', 'name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['begin_hour_device', 'work_hour']

    def get_work_hour(self, obj):
        return obj.work_hour

    def create(self, validated_data):
        device = validated_data.pop('device', None)
        if device:
            if Equipament.objects.filter(device=device).exists():
                raise serializers.ValidationError(f"Device with ID {device.device} is already associated with another Equipament.")
            validated_data['begin_hour_device'] = round(float(device.horimeter), 2)
        equipament = Equipament.objects.create(device=device, **validated_data)
        return equipament

    def update(self, instance, validated_data):
        device = validated_data.pop('device', None)
        if device and device != instance.device:
            if Equipament.objects.filter(device=device).exists():
                raise serializers.ValidationError(f"Device with ID {device.device} is already associated with another Equipament.")
            instance.device = device
            instance.begin_hour_device = round(float(device.horimeter), 2)
        
        instance.begin_hour_machine = validated_data.get('begin_hour_machine', instance.begin_hour_machine)
        
        for attr, value in validated_data.items():
            if attr not in ['begin_hour_device', 'work_hour']:
                setattr(instance, attr, value)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['device'] = DeviceSerializer(instance.device).data if instance.device else None
        return representation
