
from rest_framework import serializers
from api.models.history_model import Report, HistoricalLog, GraphData

from core.config.get_logger import get_logger

logger = get_logger()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class HistoricalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalLog
        fields = '__all__'


class GraphDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphData
        fields = '__all__'