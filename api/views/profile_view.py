from rest_framework import viewsets
from api.models.profile_model import UserProfileModel
from rest_framework.permissions import IsAuthenticated
from api.serializers.profile_serializer import UserProfileSerializer

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]
