from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models.models import Report, HistoricalLog, GraphData
from api.models.device_model import Device
from api.models.equipament_model import Equipament
from api.models.maintenance_model import Maintenance
from api.serializers import (EquipamentSerializer,
    DeviceSerializer, ReportSerializer, HistoricalLogSerializer, GraphDataSerializer,
    UserRegisterSerializer, UserSignInSerializer, MaintenanceSerializer
)
from api.monitor.get_logger import Logger

logger = Logger("smartlogger").get_logger()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSignInSerializer
    permission_classes = [AllowAny]


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)



class EquipamentViewSet(viewsets.ModelViewSet):
    queryset = Equipament.objects.all()
    serializer_class = EquipamentSerializer
    # permission_classes = [IsAuthenticated]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def get_queryset(self):
        equipament_id = self.request.query_params.get('equipament_id')
        if equipament_id:
            return Maintenance.objects.filter(equipament_id=equipament_id)
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Attempting to delete Maintenance instance: {instance.id}")
        self.perform_destroy(instance)
        logger.debug(f"Deleted Maintenance instance: {instance.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Instance deleted from database: {instance.id}")


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class HistoricalLogViewSet(viewsets.ModelViewSet):
    queryset = HistoricalLog.objects.all()
    serializer_class = HistoricalLogSerializer
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class GraphDataViewSet(viewsets.ModelViewSet):
    queryset = GraphData.objects.all()
    serializer_class = GraphDataSerializer
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
