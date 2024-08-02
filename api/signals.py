from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from api.models.base_model import Base
from api.models.device_model import Device
from api.models.equipament_model import Equipament
from api.models.maintenance_model import Maintenance
from core.config.get_logger import get_logger

logger = get_logger()

@receiver(post_save, sender=Device)
def update_equipament_on_device_save(sender, instance, **kwargs):
    try:
        equipament = Equipament.objects.get(device=instance)
        if instance.horimeter is not None:
            equipament.horimetro_inicial_suntech = float(instance.horimeter)
            equipament.save()
            # logger.info(f"Equipamento {equipament.id} atualizado com horímetro Suntech: {equipament.horimetro_inicial_suntech}")
        else:
            # logger.warning(f"Horímetro do Device {instance.id} é None.")
            return None
    except Equipament.DoesNotExist:
        # logger.warning(f"Equipamento associado ao Device {instance.id} não encontrado.")
        return None

@receiver(post_save, sender=Maintenance)
def update_equipament_on_maintenance_save(sender, instance, **kwargs):
    try:
        equipament = Equipament.objects.get(id=instance.equipament.id)
        # logger.info(f"Manutenção {instance.id} associada ao Equipamento {equipament.id}.")
        return equipament
    except Equipament.DoesNotExist:
        # logger.warning(f"Manutenção associada ao Equipamento {instance.id} não encontrada.")
        return None

@receiver(post_save, sender=Base)
def create_update_audit_log(sender, instance, created, **kwargs):
    user = kwargs.pop('user', None)
    if user:
        action = 'CREATE' if created else 'UPDATE'
        instance.log_action(action, user)
        # logger.info(f"Log de auditoria criado para {action} do {instance.__class__.__name__} {instance.id} por {user.username}")

@receiver(pre_delete, sender=Base)
def delete_audit_log(sender, instance, **kwargs):
    user = kwargs.pop('user', None)
    if user:
        instance.log_action('DELETE', user)
        # logger.info(f"Log de auditoria criado para DELETE do {instance.__class__.__name__} {instance.id} por {user.username}")
