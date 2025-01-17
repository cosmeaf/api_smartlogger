# Generated by Django 5.0.7 on 2024-08-02 01:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_graphdata_options_alter_historicallog_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maintenance',
            options={'verbose_name': 'Maintenance Record', 'verbose_name_plural': 'Maintenance Records'},
        ),
        migrations.RemoveIndex(
            model_name='maintenance',
            name='api_mainten_deleted_491a97_idx',
        ),
        migrations.AddIndex(
            model_name='maintenance',
            index=models.Index(fields=['equipament'], name='api_mainten_equipam_64f07c_idx'),
        ),
        migrations.AddIndex(
            model_name='maintenance',
            index=models.Index(fields=['name'], name='api_mainten_name_77bc80_idx'),
        ),
        migrations.AddIndex(
            model_name='maintenance',
            index=models.Index(fields=['os'], name='api_mainten_os_af85a8_idx'),
        ),
    ]
