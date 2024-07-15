# dashboard/tasks.py

from celery import shared_task
from api.monitor.converter import process_log_data
from api.models.device_model import Device, DeviceLog


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
                print(f"Merged data for device {dispositivo.device_id}: {merged_info}")
    except Exception as e:
        print(f"Erro ao mesclar dados: {e}")


@shared_task
def monitor_device_logs():
    process_log_data()


@shared_task
def update_device(device_id, data):
    try:
        device = Device.objects.get(device_id=device_id)
        for key, value in data.items():
            setattr(device, key, value)
        device.save()
        return f'Device {device_id} updated successfully'
    except Exception as e:
        return str(e)


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
                print(f"Merged data for device {dispositivo.device_id}: {merged_info}")
    except Exception as e:
        print(f"Erro ao mesclar dados: {e}")

@shared_task
def monitor_device_logs():
    process_log_data()

@shared_task
def update_device(device_id, data):
    try:
        device = Device.objects.get(device_id=device_id)
        for key, value in data.items():
            setattr(device, key, value)
        device.save()
        return f'Device {device_id} updated successfully'
    except Exception as e:
        return str(e)