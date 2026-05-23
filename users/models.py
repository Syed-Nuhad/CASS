from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Define custom user roles to separate privileges and app views
    class Role(models.TextChoices):
        RESIDENT = 'RESIDENT', 'Resident'
        DRIVER = 'DRIVER', 'Driver'
        ADMIN = 'ADMIN', 'Admin'
        
    # The user's role in the system
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESIDENT)
    
    # Track the resident's total outstanding bill for water deliveries
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True) # Primarily used for residents

    def __str__(self):
        return f"{self.username} ({self.role})"
