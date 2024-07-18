from celery import shared_task
from api.models.device_model import Device, DeviceLog
from api.monitor.converter import process_log_data
from core.config.get_logger import get_logger

logger = get_logger()

@shared_task
def mesclar_dados():
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

@shared_task
def monitor_device_logs():
    try:
        process_log_data()
        logger.info("Device logs monitored successfully")
    except Exception as e:
        logger.error(f"Erro ao monitorar logs de dispositivos: {e}")


@shared_task
def update_device(device_id, data):
    try:
        device = Device.objects.get(device_id=device_id)
        for key, value in data.items():
            setattr(device, key, value)
        device.save()
        logger.info(f"Device {device_id} updated successfully")
        return f'Device {device_id} updated successfully'
    except Exception as e:
        logger.error(f"Erro ao atualizar dispositivo {device_id}: {e}")
        return str(e)
