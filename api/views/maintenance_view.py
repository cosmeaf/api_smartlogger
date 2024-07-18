from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
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
            return Maintenance.objects.filter(equipament_id=equipament_id, deleted_at__isnull=True)
        return Maintenance.objects.filter(deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Attempting to delete Maintenance instance: {instance.id}")
        self.perform_destroy(instance, request.user)
        logger.debug(f"Deleted Maintenance instance: {instance.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance, user):
        instance.delete(user=user)
        logger.debug(f"Instance marked as deleted in the database: {instance.id}")

    @action(detail=True, methods=['post'])
    def reset_usage_hours(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.reset_usage_hours()
            return Response({'status': 'usage hours reset'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to reset usage hours for Maintenance instance: {pk}", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
