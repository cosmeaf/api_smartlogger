from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from api.models.maintenance_model import Maintenance
from api.serializers.maintenance_serializer import MaintenanceSerializer
import logging

logger = logging.getLogger(__name__)

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        equipament_id = self.request.query_params.get('equipament_id')
        if equipament_id:
            logger.info(f"Filtering Maintenance by equipament_id: {equipament_id}")
            return Maintenance.objects.filter(equipament_id=equipament_id)
        return Maintenance.objects.all()

    @method_decorator(cache_page(15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Attempting to delete Maintenance instance: {instance.id}")
        self.perform_destroy(instance)
        logger.debug(f"Deleted Maintenance instance: {instance.id}")
        cache.clear()  # Clear the cache
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Instance marked as deleted in the database: {instance.id}")

    @action(detail=True, methods=['post'])
    def reset_usage_hours(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.reset_usage_hours()
        logger.info(f"Reset usage hours for Maintenance ID {maintenance.id}")
        cache.clear()  # Clear the cache
        return Response(status=status.HTTP_200_OK)
