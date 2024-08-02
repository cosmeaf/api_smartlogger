from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from api.models.profile_model import UserProfileModel
from api.serializers.profile_serializer import UserProfileSerializer
import logging

logger = logging.getLogger(__name__)

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(f"Attempting to delete UserProfile instance: {instance.id}")
        self.perform_destroy(instance)
        logger.debug(f"Deleted UserProfile instance: {instance.id}")
        cache.clear()  # Clear the cache
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Instance marked as deleted in the database: {instance.id}")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.clear()  # Clear the cache
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        cache.clear()  # Clear the cache
        return response
