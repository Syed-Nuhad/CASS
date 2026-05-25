from django.core.mail import send_mail
from django.conf import settings
from webpush import send_user_notification
from .models import InAppNotification
from alerts.utils import send_emergency_sms

def send_omnichannel_notification(user, title, message):
    """
    Dispatches a notification via 3 channels:
    1. Email (SMTP / Console)
    2. SMS (Twilio / Mock)
    3. In-App Notification (Database)
    4. Web Push (Browser)
    """
    
    # 1. Email
    if user.email:
        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass

    # 2. SMS
    if hasattr(user, 'phone_number') and user.phone_number:
        try:
            send_emergency_sms(user.phone_number, f"{title}\n{message}")
        except Exception:
            pass

    # 3. In-App Notification
    try:
        InAppNotification.objects.create(
            user=user,
            title=title,
            message=message
        )
    except Exception:
        pass

    # 4. Web Push Notification
    payload = {
        'head': title,
        'body': message,
        'icon': 'https://i.imgur.com/dZ1Bq4i.png'
    }
    try:
        send_user_notification(user=user, payload=payload, ttl=1000)
    except Exception:
        pass
