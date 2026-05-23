from django.urls import path
from .views import broadcast_alert_view

urlpatterns = [
    path('broadcast/', broadcast_alert_view, name='broadcast_alert'),
]
