from rest_framework import serializers
from api.models.equipament_model import Equipament
from api.models.device_model import Device

class EquipamentSerializer(serializers.ModelSerializer):
    device = serializers.CharField(write_only=True, required=True)
    horas_trabalhadas = serializers.SerializerMethodField()

    class Meta:
        model = Equipament
        fields = [
            'id', 'device', 'horas_trabalhadas', 'horimetro_inicialSuntech', 'horimetro_inicialMaquina', 'nome', 'ano', 'numero_serie',
            'modelo', 'ponto_medicao', 'combustivel', 'numero_pulsos', 'perimetro_pneu', 'horas_disponiveis_mes',
            'consumo_medio', 'alerta_velocidade', 'alerta_temperatura', 'alerta_shock', 'horas_efetivas_hodometro',
            'hodometro', 'obs', 'updated_at'
        ]

    def get_horas_trabalhadas(self, obj):
        return obj.horas_trabalhadas

    def validate_device(self, value):
        if not Device.objects.filter(device_id=value).exists():
            raise serializers.ValidationError("Identificação do dispositivo inválida. Verifique o 'device_id'.")
        return value

    def create(self, validated_data):
        device_id = validated_data.pop('device')
        try:
            device = Device.objects.get(device_id=device_id)
            if Equipament.objects.filter(device=device).exists():
                equipament = Equipament.objects.get(device=device)
                raise serializers.ValidationError(f"Device with GPS {device_id} is already associated with Equipament {equipament.nome}.")
            validated_data['device'] = device
            validated_data['horimetro_inicialSuntech'] = round(float(device.horimeter), 2)
        except Device.DoesNotExist:
            raise serializers.ValidationError(f"Device with GPS {device_id} does not exist.")
        
        equipament = Equipament.objects.create(**validated_data)
        return equipament

    def update(self, instance, validated_data):
        device_id = validated_data.pop('device', None)
        if device_id:
            try:
                device = Device.objects.get(device_id=device_id)
                if device != instance.device and Equipament.objects.filter(device=device).exists():
                    equipament = Equipament.objects.get(device=device)
                    raise serializers.ValidationError(f"Device with GPS {device_id} is already associated with Equipament {equipament.nome}.")
                instance.device = device
                instance.horimetro_inicialSuntech = round(float(device.horimeter), 2)
            except Device.DoesNotExist:
                raise serializers.ValidationError(f"Device with GPS {device_id} does not exist.")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['device'] = instance.device.device_id
        return representation
