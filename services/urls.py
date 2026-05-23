from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaterRequestViewSet, MaintenanceRequestViewSet

router = DefaultRouter()
router.register(r'water', WaterRequestViewSet)
router.register(r'maintenance', MaintenanceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
