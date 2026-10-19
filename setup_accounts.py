import os
import sys
import django

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cass_backend.settings')
os.environ['CASS_DISABLE_MACHINE_LOCK'] = '1'

# Insert project path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

django.setup()

from users.models import User
from services.models import SystemSettings

def setup_demo_accounts():
    print("============================================================")
    print("[*] CASS Account Setup & Credential Verifier")
    print("============================================================")

    # Disable MFA for local development convenience if desired
    settings = SystemSettings.get_settings()
    if settings.enable_staff_mfa:
        settings.enable_staff_mfa = False
        settings.save()
        print("[+] Disabled Staff MFA for local development convenience.")

    # Reset Axes Brute-Force Lockouts
    try:
        from axes.models import AccessAttempt, AccessFailureLog
        AccessAttempt.objects.all().delete()
        AccessFailureLog.objects.all().delete()
        print("[+] Unlocked all accounts: reset django-axes lockout.")
    except Exception as e:
        pass

    accounts = [
        {
            'username': 'admin',
            'email': 'admin@cass.local',
            'password': 'password123',
            'role': 'ADMIN',
            'is_superuser': True,
            'is_staff': True,
            'phone': '+12465550001',
            'desc': 'Dispatch Center & Admin Console'
        },
        {
            'username': 'john_resident',
            'email': 'resident@cass.local',
            'password': 'password123',
            'role': 'RESIDENT',
            'is_superuser': False,
            'is_staff': False,
            'phone': '+12465550002',
            'desc': 'Customer Portal (Resident App)'
        },
        {
            'username': 'driver1',
            'email': 'driver1@cass.local',
            'password': 'password123',
            'role': 'DRIVER',
            'is_superuser': False,
            'is_staff': False,
            'phone': '+12465550003',
            'desc': 'Driver Logistics Hub'
        },
        {
            'username': 'staff_inventory',
            'email': 'inventory@cass.local',
            'password': 'password123',
            'role': 'STAFF_INVENTORY',
            'is_superuser': False,
            'is_staff': True,
            'phone': '+12465550004',
            'desc': 'Inventory Depot'
        },
        {
            'username': 'staff_accounts',
            'email': 'accounts@cass.local',
            'password': 'password123',
            'role': 'STAFF_ACCOUNTS',
            'is_superuser': False,
            'is_staff': True,
            'phone': '+12465550005',
            'desc': 'Accounts & Financial Ledger'
        }
    ]

    for acc in accounts:
        user = User.objects.filter(username=acc['username']).first()
        if not user:
            user = User.objects.create_user(
                username=acc['username'],
                email=acc['email'],
                password=acc['password'],
                role=acc['role'],
                is_superuser=acc['is_superuser'],
                is_staff=acc['is_staff'],
                phone_number=acc['phone']
            )
            status = "[+] CREATED"
        else:
            user.set_password(acc['password'])
            user.role = acc['role']
            user.is_superuser = acc['is_superuser']
            user.is_staff = acc['is_staff']
            if not user.email:
                user.email = acc['email']
            user.save()
            status = "[*] UPDATED"

        print(f"{status} {acc['username']:<16} | Password: {acc['password']} | {acc['desc']}")

    print("============================================================")
    print("[SUCCESS] All accounts are set up with password: password123")
    print("============================================================")

if __name__ == '__main__':
    setup_demo_accounts()
