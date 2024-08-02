from celery import shared_task
from django.db import transaction
from api.models.device_model import Device, DeviceLog
from api.models.maintenance_model import Maintenance
from api.monitor.converter import process_log_data
from core.config.get_logger import get_logger

logger = get_logger()

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def update_device(self, device_id, data):
    try:
        with transaction.atomic():
            device = Device.objects.select_for_update().get(device_id=device_id)
            for key, value in data.items():
                setattr(device, key, value)
            device.save()
        logger.info(f"Device {device.device_id} updated successfully")
        return f'Device {device.device_id} updated successfully'
    except Exception as e:
        logger.error(f"Erro ao atualizar dispositivo {device_id}: {e}")
        self.retry(exc=e)

@shared_task
def process_device_updates():
    try:
        devices = Device.objects.all()
        for device in devices:
            try:
                data = {field.name: getattr(device, field.name) for field in device._meta.fields if field.name != 'id'}
                logger.info(f"Enviando atualização para o dispositivo {device.device_id}")
                update_device.delay(device.device_id, data)
            except Exception as e:
                logger.error(f"Erro ao processar dispositivo {device.device_id}: {e}")
    except Exception as e:
        logger.error(f"Erro ao buscar dispositivos: {e}")

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def mesclar_dados(self):
    try:
        dispositivos = Device.objects.all()
        for dispositivo in dispositivos:
            logs_dispositivo = DeviceLog.objects.filter(device=dispositivo)
            for log in logs_dispositivo:
                merged_info = f"{dispositivo.name} - {log.timestamp}"
                log.additional_info = merged_info
                log.save()
                logger.info(f"Merged data for device {dispositivo.device_id}: {merged_info}")
    except Exception as e:
        logger.error(f"Erro ao mesclar dados: {e}")
        self.retry(exc=e)

@shared_task
def monitor_device_logs():
    try:
        process_log_data()
        logger.info("Device logs monitored successfully")
    except Exception as e:
        logger.error(f"Erro ao monitorar logs de dispositivos: {e}")

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def monitor_maintenance_status(self):
    try:
        maintenances = Maintenance.objects.all()
        for maintenance in maintenances:
            background_color = maintenance.background_color
            logger.info(f"Monitoring Maintenance - OS status: {maintenance.os}, Background color: {background_color}")
    except Exception as e:
        logger.error(f"Erro ao monitorar status de manutenção: {e}")
        self.retry(exc=e)
