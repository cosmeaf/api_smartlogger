import os
import uuid
from django.db import models
from api.models.base_model import Base
from api.models.equipament_model import Equipament

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile', filename)

class UserProfileModel(Base):
    equipament = models.ForeignKey(Equipament, on_delete=models.CASCADE, related_name='user_profiles')
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField('Imagem Perfil', upload_to=get_file_path, null=True, blank=True)
    bio = models.TextField('Biografia', max_length=500, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=18, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    @property
    def device_id(self):
        if self.equipament and self.equipament.device:
            return self.equipament.device.device_id
        return None

    @property
    def rfid(self):
        if self.equipament and self.equipament.device:
            return self.equipament.device.rfid
        return None

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.id})'
