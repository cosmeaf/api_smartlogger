# Generated by Django 5.0.7 on 2024-07-20 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_maintenance_horimetro_inicial_peca'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='horimetro_inicialMaintenance',
            field=models.FloatField(default=0, verbose_name='AZ Hora Máquina'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='horimetro_inicialSuntech',
            field=models.FloatField(default=0, verbose_name='Ajuste de Zero Hora Suntech'),
        ),
    ]
