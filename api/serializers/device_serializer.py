from rest_framework import serializers
from api.models.device_model import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id']