from django.contrib import admin
from .models import WaterRequest, MaintenanceRequest, SystemSettings, Inventory

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

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('price_per_liter', 'delivery_fee', 'urgent_surcharge', 'critical_surcharge', 'is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the last remaining pricing row
        if obj is not None and SystemSettings.objects.count() <= 1:
            return False
        return True

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('total_water_liters', 'last_updated')
    
    def has_add_permission(self, request):
        # Prevent creating multiple inventory rows
        if Inventory.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the inventory
        return False
