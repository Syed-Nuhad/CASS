from rest_framework import serializers
from .models import WaterRequest, MaintenanceRequest

class WaterRequestSerializer(serializers.ModelSerializer):
    resident_name = serializers.ReadOnlyField(source='resident.username')
    driver_name = serializers.ReadOnlyField(source='driver.username')

    class Meta:
        model = WaterRequest
        fields = '__all__'
        read_only_fields = ('resident', 'status', 'created_at', 'updated_at')

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    resident_name = serializers.ReadOnlyField(source='resident.username')

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ('resident', 'status', 'created_at', 'updated_at')
