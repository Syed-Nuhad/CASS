from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class WaterRequest(models.Model):
    # Enum for priority levels
    class Priority(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal'
        URGENT = 'URGENT', 'Urgent'
        CRITICAL = 'CRITICAL', 'Critical'

    # Enum for delivery status tracking
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        FORWARDED = 'FORWARDED', 'Forwarded to Hub'
        ON_THE_WAY = 'ON_THE_WAY', 'On The Way'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # Relationships
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='water_requests')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='water_deliveries')
    
    # Request Details
    volume_liters = models.IntegerField()
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Optional resident attachments
    note = models.TextField(blank=True, help_text="Optional instructions for the driver")
    photo = models.ImageField(upload_to='water_requests/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_cost(self):
        """Calculates the cost based on volume, priority, and active system settings."""
        settings = SystemSettings.get_settings()
        base_cost = self.volume_liters * float(settings.price_per_liter)
        delivery_fee = float(settings.delivery_fee)
        surcharge = 0.0
        if self.priority == 'URGENT':
            surcharge = float(settings.urgent_surcharge)
        elif self.priority == 'CRITICAL':
            surcharge = float(settings.critical_surcharge)
        return base_cost + delivery_fee + surcharge

    def save(self, *args, **kwargs):
        # Auto-calculate cost before saving if not explicitly set or is 0
        if not self.cost or self.cost == 0:
            self.cost = self.calculate_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Water {self.id} - {self.resident.username} - {self.status}"

class MaintenanceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'

    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='maintenance_requests')
    
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    photo_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance {self.id} - {self.resident.username}"

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"${self.amount} - {self.description} ({self.date.strftime('%Y-%m-%d')})"

class InAppNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='in_app_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.user.username}: {self.title}"

@receiver(post_save, sender=WaterRequest)
@receiver(post_save, sender=MaintenanceRequest)
def broadcast_request_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_updates',
        {
            'type': 'dashboard_message',
            'message': 'update'
        }
    )


class SystemSettings(models.Model):
    """Each row is a pricing rate. Mark one as Active to make it the live price."""
    price_per_liter = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0500,
        help_text="Base price per liter of water (e.g. 0.0500 = $0.05)"
    )
    urgent_surcharge = models.DecimalField(
        max_digits=8, decimal_places=2, default=15.00,
        help_text="Extra flat fee added for Urgent priority requests"
    )
    critical_surcharge = models.DecimalField(
        max_digits=8, decimal_places=2, default=50.00,
        help_text="Extra flat fee added for Critical priority requests"
    )
    delivery_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=10.00,
        help_text="Flat fee charged for the delivery itself"
    )

    branding_logo = models.ImageField(
        upload_to='branding/', null=True, blank=True,
        help_text="Global organization logo used in footer, favicon, and PDF reports."
    )
    
    company_address = models.CharField(max_length=255, null=True, blank=True, help_text="Company address displayed in the footer")
    company_email = models.EmailField(null=True, blank=True, help_text="Company contact email displayed in the footer")
    company_phone = models.CharField(max_length=50, null=True, blank=True, help_text="Company contact phone displayed in the footer")

    is_active = models.BooleanField(
        default=False,
        help_text="Only ONE rate can be active at a time. This is the rate used for all new requests."
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "System Pricing Settings"
        verbose_name_plural = "System Pricing Settings"
        ordering = ['-created_at']

    def __str__(self):
        status = "✅ ACTIVE" if self.is_active else "⏸ Inactive"
        return f"{status} | ${self.price_per_liter}/L | Delivery +${self.delivery_fee} | Urgent +${self.urgent_surcharge} | Critical +${self.critical_surcharge}"

    def save(self, *args, **kwargs):
        from django.core.cache import cache
        # If this row is being set to active, deactivate all other rows first
        if self.is_active:
            SystemSettings.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
        cache.delete('system_settings')

    def delete(self, *args, **kwargs):
        from django.core.cache import cache
        super().delete(*args, **kwargs)
        cache.delete('system_settings')

    @classmethod
    def get_settings(cls):
        """Return the active pricing row, or fall back to the most recent, using Django Cache."""
        from django.core.cache import cache
        obj = cache.get('system_settings')
        if obj is None:
            obj = cls.objects.filter(is_active=True).first()
            if obj is None:
                obj = cls.objects.first()
            if obj is None:
                obj = cls.objects.create(is_active=True)
            # Store in cache for 24 hours
            cache.set('system_settings', obj, timeout=86400)
        return obj


class Inventory(models.Model):
    """Singleton model to track total available water inventory in liters."""
    total_water_liters = models.BigIntegerField(
        default=0,
        help_text="Total water available in the facility (in liters)"
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Water Inventory"
        verbose_name_plural = "Water Inventory"

    def __str__(self):
        return f"Current Inventory: {self.total_water_liters} Liters"

    @classmethod
    def get_inventory(cls):
        """Always return the single inventory row, creating it if necessary."""
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(total_water_liters=0)
        return obj
