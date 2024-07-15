# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from api.views import (UserRegisterView, UserTokenObtainPairView, EquipamentViewSet,
                       DeviceViewSet, ReportViewSet, HistoricalLogViewSet, GraphDataViewSet,
                       MaintenanceViewSet,)

router = DefaultRouter()
router.register(r'equipament', EquipamentViewSet)
router.register(r'device', DeviceViewSet)
router.register(r'maintenance', MaintenanceViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'historical_logs', HistoricalLogViewSet)
router.register(r'graph_data', GraphDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
