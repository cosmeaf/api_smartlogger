from rest_framework import serializers
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation
from api.models.models import Report, HistoricalLog, GraphData
from api.models.device_model import Device
from api.models.equipament_model import Equipament
from api.models.maintenance_model import Maintenance
from rest_framework_simplejwt.tokens import RefreshToken
from api.monitor.get_logger import Logger

logger = Logger("smartlogger").get_logger()


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 30

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Endereço de email já está em uso.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("E-mail não registrado.")

        user_authenticated = authenticate(username=email, password=password)

        if user_authenticated:
            user.failed_login_attempts = 0
            user.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access': str(refresh.access_token),
                'refresh': str(refresh), 
            }
            return response_data
        else:
            user.failed_login_attempts += 1
            user.last_failed_login = datetime.now()
            user.save()

            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                lockout_time = timedelta(minutes=LOCKOUT_TIME)
                current_time = datetime.now()

                if user.last_failed_login and (current_time - user.last_failed_login) > lockout_time:
                    user.failed_login_attempts = 0
                    user.save()
                else:
                    logger.info("Muitas tentativas de login. Tente novamente em {} minutos.".format(LOCKOUT_TIME))
                    raise serializers.ValidationError("Muitas tentativas de login. Tente novamente em {} minutos.".format(LOCKOUT_TIME))

            raise serializers.ValidationError("Unable to log in with provided credentials.",code='authentication_failed')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id']


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


class MaintenanceSerializer(serializers.ModelSerializer):
    remaining_hours = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = ['id', 'equipament', 'name', 'os', 'usage_hours', 'alarm_hours', 'obs', 'remaining_hours']

    def get_remaining_hours(self, obj):
        return obj.remaining_hours

    def create(self, validated_data):
        equipament = validated_data.get('equipament')
        validated_data['usage_hours'] = float(equipament.device.horimeter) - validated_data['alarm_hours']
        return super().create(validated_data)
    

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class HistoricalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalLog
        fields = '__all__'


class GraphDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphData
        fields = '__all__'
