from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        RESIDENT = 'RESIDENT', 'Resident'
        DRIVER = 'DRIVER', 'Driver'
        ADMIN = 'ADMIN', 'Admin'
        
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESIDENT)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True) # Primarily used for residents

    def __str__(self):
        return f"{self.username} ({self.role})"
