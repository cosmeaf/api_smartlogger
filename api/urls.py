from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.auth_view import UserRegisterView, UserLoginView
from api.views.test_email_view import TestEmailView
from api.views.device_view import DeviceViewSet
from api.views.equipament_view import EquipamentViewSet
from api.views.maintenance_view import MaintenanceViewSet
from api.views.profile_view import UserProfileView
from api.views.history_view import ReportViewSet, HistoricalLogViewSet, GraphDataViewSet
from api.views.social_view import FacebookUserDeletionCallbackView



router = DefaultRouter()
router.register(r'device', DeviceViewSet)
router.register(r'equipament', EquipamentViewSet)
router.register(r'maintenance', MaintenanceViewSet)
router.register(r'profile', UserProfileView)
router.register(r'reports', ReportViewSet)
router.register(r'historical_logs', HistoricalLogViewSet)
router.register(r'graph_data', GraphDataViewSet)

urlpatterns = [
    path('api/test-email/', TestEmailView.as_view(), name='test-email'),
    path('api/register/', UserRegisterView.as_view(), name='sign-up'),
    path('api/token/', UserLoginView.as_view(), name='sign-in'),
    path('api/facebook/delete_user/', FacebookUserDeletionCallbackView.as_view(), name='facebook-delete-user'),

    path('api/', include(router.urls)),
]
