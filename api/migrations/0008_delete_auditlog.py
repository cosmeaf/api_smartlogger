# Generated by Django 5.0.7 on 2024-07-18 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auditlog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuditLog',
        ),
    ]
