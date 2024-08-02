# Generated by Django 5.0.7 on 2024-08-01 21:02

import api.models.equipament_model
import api.models.profile_model
import django.db.models.deletion
import django.utils.timezone
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_backend', models.CharField(choices=[('django.core.mail.backends.smtp.EmailBackend', 'SMTP'), ('django.core.mail.backends.console.EmailBackend', 'Console')], default='django.core.mail.backends.smtp.EmailBackend', max_length=255)),
                ('email_service', models.CharField(blank=True, choices=[('Gmail', 'Gmail'), ('Outlook', 'Outlook'), ('Yahoo Mail', 'Yahoo Mail'), ('Zoho Mail', 'Zoho Mail'), ('GMX', 'GMX'), ('AOL Mail', 'AOL Mail'), ('ProtonMail', 'ProtonMail'), ('SMTP2GO', 'SMTP2GO'), ('SendPulse', 'SendPulse'), ('MailerSend', 'MailerSend'), ('Mailtrap', 'Mailtrap'), ('Postmark', 'Postmark'), ('SendGrid', 'SendGrid'), ('Manual', 'Manual')], max_length=255, null=True)),
                ('email_host', models.CharField(blank=True, max_length=255, null=True)),
                ('email_port', models.IntegerField(blank=True, null=True)),
                ('email_use_tls', models.BooleanField(default=True)),
                ('email_host_user', models.EmailField(blank=True, max_length=254, null=True)),
                ('email_host_password', models.CharField(blank=True, max_length=255, null=True)),
                ('default_from_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalMyModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('history_date', models.DateTimeField(auto_now_add=True, verbose_name='Data do Histórico')),
                ('history_change_reason', models.CharField(blank=True, max_length=100, verbose_name='Razão da Mudança')),
            ],
            options={
                'verbose_name': 'Histórico do Meu Modelo',
                'verbose_name_plural': 'Históricos dos Meus Modelos',
                'ordering': ['-history_date'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('HDR', models.CharField(blank=True, max_length=50, null=True)),
                ('device_id', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Identificador')),
                ('report_map', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('software_version', models.CharField(blank=True, max_length=50, null=True)),
                ('message_type', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.CharField(blank=True, max_length=50, null=True)),
                ('hora', models.CharField(blank=True, max_length=50, null=True)),
                ('latitude', models.CharField(blank=True, max_length=50, null=True)),
                ('longitude', models.CharField(blank=True, max_length=50, null=True)),
                ('speed_gps', models.CharField(blank=True, max_length=50, null=True)),
                ('course', models.CharField(blank=True, max_length=50, null=True)),
                ('satellites', models.CharField(blank=True, max_length=50, null=True)),
                ('fix_status', models.CharField(blank=True, max_length=50, null=True)),
                ('in_state', models.CharField(blank=True, max_length=50, null=True)),
                ('out_state', models.CharField(blank=True, max_length=50, null=True)),
                ('mode', models.CharField(blank=True, max_length=50, null=True)),
                ('report_type', models.CharField(blank=True, max_length=50, null=True)),
                ('message_number', models.CharField(blank=True, max_length=50, null=True)),
                ('reserved', models.CharField(blank=True, max_length=50, null=True)),
                ('assign_map', models.CharField(blank=True, max_length=50, null=True)),
                ('power_voltage', models.FloatField(blank=True, null=True)),
                ('bateria_suntech', models.FloatField(blank=True, null=True)),
                ('connection_rat', models.CharField(blank=True, max_length=50, null=True)),
                ('acceleration_x', models.FloatField(blank=True, null=True)),
                ('acceleration_y', models.FloatField(blank=True, null=True)),
                ('acceleration_z', models.FloatField(blank=True, null=True)),
                ('ADC', models.CharField(blank=True, max_length=50, null=True)),
                ('GPS_odometer', models.CharField(blank=True, max_length=50, null=True)),
                ('trip_distance', models.CharField(blank=True, max_length=50, null=True)),
                ('horimeter', models.CharField(default='0', max_length=100)),
                ('trip_horimeter', models.CharField(blank=True, max_length=50, null=True)),
                ('idle_time', models.CharField(blank=True, max_length=50, null=True)),
                ('impact', models.FloatField(blank=True, null=True)),
                ('SoC_battery_voltage', models.FloatField(blank=True, null=True)),
                ('temperatura', models.FloatField(blank=True, null=True)),
                ('data_length', models.CharField(blank=True, max_length=50, null=True)),
                ('RFID', models.CharField(blank=True, max_length=50, null=True)),
                ('velocidade_instantanea', models.CharField(blank=True, max_length=50, null=True)),
                ('velocidade_pico', models.CharField(blank=True, max_length=50, null=True)),
                ('temperatura_instantanea', models.CharField(blank=True, max_length=50, null=True)),
                ('temperatura_pico', models.CharField(blank=True, max_length=50, null=True)),
                ('alert_id', models.CharField(blank=True, max_length=50, null=True)),
                ('alert_modifier', models.CharField(blank=True, max_length=50, null=True)),
                ('alert_data', models.CharField(blank=True, max_length=50, null=True)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('additional_info', models.CharField(blank=True, max_length=255, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.device')),
            ],
            options={
                'verbose_name_plural': 'Device Logs',
            },
        ),
        migrations.CreateModel(
            name='Equipament',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('begin_hour_device', models.FloatField(default=0, verbose_name='Ajuste de Zero Hora Suntech')),
                ('begin_hour_machine', models.FloatField(default=0, verbose_name='AZ Hora Máquina')),
                ('total_hour_meter', models.FloatField(default=0, editable=False, verbose_name='Horímetro Total')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('year', models.IntegerField(blank=True, default=api.models.equipament_model.current_year, null=True, verbose_name='Ano')),
                ('model', models.CharField(blank=True, default='N/A', max_length=255, null=True, verbose_name='Modelo')),
                ('measuring_point', models.CharField(blank=True, default='N/A', max_length=255, null=True, verbose_name='Ponto de Medição')),
                ('fuel', models.CharField(blank=True, default='DIESEL', max_length=8, null=True, verbose_name='Combustível')),
                ('pulse_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Número de Pulsos')),
                ('tire_perimeter', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Perímetro do Pneu (cm)')),
                ('available_hours_per_month', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Horas Disponíveis por Mês')),
                ('average_consumption', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Consumo Médio (m³/h - L/h - Kg/h)')),
                ('speed_alert', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Alerta de Velocidade (km/h)')),
                ('temperature_alert', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Alerta de Temperatura (°C)')),
                ('shock_alert', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Alerta de Shock (km/h)')),
                ('effective_hours_odometer', models.CharField(blank=True, default='HODOMETRO', max_length=255, null=True, verbose_name='Horas Efetivas ou Hodômetro')),
                ('odometer', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Hodômetro')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='api.device')),
            ],
            options={
                'verbose_name': 'Equipamento',
                'verbose_name_plural': 'Equipamentos',
            },
        ),
        migrations.CreateModel(
            name='GraphData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('period', models.CharField(choices=[('1_month', '1 Month'), ('3_months', '3 Months'), ('6_months', '6 Months'), ('12_months', '12 Months')], max_length=50)),
                ('data_type', models.CharField(choices=[('fuel_consumption', 'Fuel Consumption'), ('working_hours', 'Working Hours'), ('maintenance', 'Maintenance'), ('alerts', 'Alerts')], max_length=50)),
                ('data', models.JSONField()),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.device')),
                ('equipament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.equipament')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.JSONField()),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('horimetro_inicial_suntech', models.FloatField(default=0, verbose_name='Ajuste de Zero Hora Suntech')),
                ('horimetro_inicial_maintenance', models.FloatField(default=0, verbose_name='AZ Hora Máquina')),
                ('name', models.CharField(max_length=255)),
                ('os', models.BooleanField(default=False)),
                ('usage_hours', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('alarm_hours', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('obs', models.TextField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('equipament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenances', to='api.equipament')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('name', models.CharField(max_length=255)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('report_type', models.CharField(choices=[('fuel_consumption', 'Fuel Consumption'), ('working_hours', 'Working Hours'), ('maintenance', 'Maintenance'), ('alerts', 'Alerts')], max_length=50)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('generated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfileModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to=api.models.profile_model.get_file_path, verbose_name='Imagem Perfil')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='Biografia')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=18, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('equipament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='api.equipament')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['device_id'], name='api_device_device__121d16_idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['horimeter'], name='api_device_horimet_4b4b3f_idx'),
        ),
        migrations.AddIndex(
            model_name='devicelog',
            index=models.Index(fields=['device', 'timestamp'], name='api_devicel_device__6d2e3e_idx'),
        ),
        migrations.AddIndex(
            model_name='equipament',
            index=models.Index(fields=['device', 'name'], name='api_equipam_device__b28981_idx'),
        ),
    ]
