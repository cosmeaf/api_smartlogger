
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.equipament_model import Equipament
from api.serializers.equipament_serialize import EquipamentSerializer


class EquipamentViewSet(viewsets.ModelViewSet):
    queryset = Equipament.objects.all()
    serializer_class = EquipamentSerializer
    # permission_classes = [IsAuthenticated]