import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cass_backend.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User



# Create a test Resident
resident, created = User.objects.get_or_create(
    username='john_resident',
    defaults={
        'email': 'resident@example.com',
        'password': make_password('testpass123'),
        'role': 'RESIDENT',
        'phone_number': '+15551234567'
    }
)
if not created:
    resident.password = make_password('testpass123')
    resident.role = 'RESIDENT'
    resident.save()

# Create a test Driver
driver, created = User.objects.get_or_create(
    username='mike_driver',
    defaults={
        'email': 'driver@example.com',
        'password': make_password('testpass123'),
        'role': 'DRIVER',
        'phone_number': '+15559876543'
    }
)
if not created:
    driver.password = make_password('testpass123')
    driver.role = 'DRIVER'
    driver.save()

print("Test users created successfully!")
print("Resident: john_resident / testpass123")
print("Driver: mike_driver / testpass123")
