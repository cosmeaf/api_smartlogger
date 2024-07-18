# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from api.models.base_model import Base

@receiver(post_save, sender=Base)
def create_update_audit_log(sender, instance, created, **kwargs):
    user = kwargs.pop('user', None)
    if user:
        action = 'CREATE' if created else 'UPDATE'
        instance.log_action(action, user)

@receiver(pre_delete, sender=Base)
def delete_audit_log(sender, instance, **kwargs):
    user = kwargs.pop('user', None)
    if user:
        instance.log_action('DELETE', user)
