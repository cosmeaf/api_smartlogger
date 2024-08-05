from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from api.models.equipament_model import Equipament
from api.serializers.equipament_serialize import EquipamentReadSerializer, EquipamentWriteSerializer
from rest_framework.permissions import IsAuthenticated

class EquipamentViewSet(viewsets.ModelViewSet):
    queryset = Equipament.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EquipamentReadSerializer
        return EquipamentWriteSerializer

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
