from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from api.models.device_model import Device
from rest_framework.permissions import IsAuthenticated
from api.serializers.device_serializer import DeviceSerializer


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
