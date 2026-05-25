import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cass_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def create_or_reset(username, password, role):
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.role = role
    
    if role.startswith('STAFF_') or role == 'ADMIN':
        user.is_staff = True
        if role == 'ADMIN':
            user.is_superuser = True
    
    user.save()
    return created

# Create standard test accounts
create_or_reset('driver1', 'password123', 'DRIVER')
create_or_reset('inventory_staff', 'password123', 'STAFF_INVENTORY')
create_or_reset('accounts_staff', 'password123', 'STAFF_ACCOUNTS')

print("Test accounts successfully created/reset.")
