from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models.history_model import Report, HistoricalLog, GraphData
from api.serializers.history_serializer import (ReportSerializer, HistoricalLogSerializer, GraphDataSerializer,)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class HistoricalLogViewSet(viewsets.ModelViewSet):
    queryset = HistoricalLog.objects.all()
    serializer_class = HistoricalLogSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class GraphDataViewSet(viewsets.ModelViewSet):
    queryset = GraphData.objects.all()
    serializer_class = GraphDataSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)