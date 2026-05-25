from django.contrib import admin
from django.urls import path, include
from services.views import dashboard_view, resident_mobile_view, driver_mobile_view, service_worker_view, driver_order_detail_view, staff_inventory_view, accounts_dashboard_view, export_financial_pdf_view, mark_notifications_read_view
from users.views import login_view, register_view, logout_view, driver_login_view, driver_register_view, staff_login_view, staff_create_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import app_secrets

urlpatterns = [
    path(app_secrets.ADMIN_URL_PATH, admin.site.urls),
    path('webpush/', include('webpush.urls')),
    path('api/services/', include('services.urls')),
    path('alerts/', include('alerts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/notifications/read/', mark_notifications_read_view, name='mark_notifications_read'),
    path('app/', resident_mobile_view, name='resident_app'),
    path('driver/', driver_mobile_view, name='driver_app'),
    path('driver/order/<int:pk>/', driver_order_detail_view, name='driver_order_detail'),
    path('sw.js', service_worker_view, name='service_worker'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('driver/login/', driver_login_view, name='driver_login'),
    path('driver/register/', driver_register_view, name='driver_register'),
    path('staff/login/', staff_login_view, name='staff_login'),
    path('staff/create/', staff_create_view, name='staff_create'),
    path('staff/inventory/', staff_inventory_view, name='staff_inventory'),
    path('staff/accounts/', accounts_dashboard_view, name='accounts_dashboard'),
    path('staff/accounts/export/', export_financial_pdf_view, name='export_financial_pdf'),
    path('', dashboard_view, name='dashboard'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
