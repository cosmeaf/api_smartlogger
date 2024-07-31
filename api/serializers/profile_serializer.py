from rest_framework import serializers
from api.models.profile_model import UserProfileModel
from api.models.equipament_model import Equipament

class UserProfileSerializer(serializers.ModelSerializer):
    device_id = serializers.SerializerMethodField()
    rfid = serializers.SerializerMethodField()
    equipament_id = serializers.PrimaryKeyRelatedField(queryset=Equipament.objects.all(), source='equipament')

    class Meta:
        model = UserProfileModel
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'image',
            'bio',
            'birthday',
            'phone_number',
            'department',
            'position',
            'hire_date',
            'device_id',
            'rfid',
            'equipament_id',
        ]

    def get_device_id(self, obj):
        if obj.equipament and obj.equipament.device:
            return obj.equipament.device.device_id
        return None

    def get_rfid(self, obj):
        if obj.equipament and obj.equipament.device:
            return obj.equipament.device.RFID
        return None
