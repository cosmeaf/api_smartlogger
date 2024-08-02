from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from api.serializers.auth_serializer import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    @method_decorator(cache_page(15))  # Cache por 15 segundos
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
