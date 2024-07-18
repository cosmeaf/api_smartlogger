from rest_framework import generics
from api.serializers.auth_serializer import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
