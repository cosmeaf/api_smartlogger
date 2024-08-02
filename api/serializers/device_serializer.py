from rest_framework import serializers # type: ignore
from api.models.device_model import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ['id']