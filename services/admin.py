from django.contrib import admin
from .models import WaterRequest, MaintenanceRequest

@admin.register(WaterRequest)
class WaterRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'driver', 'priority', 'status', 'volume_liters', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('resident__username', 'driver__username')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('resident__username',)
