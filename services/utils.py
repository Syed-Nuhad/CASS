from django.core.mail import send_mail
from django.conf import settings
from webpush import send_user_notification
from .models import InAppNotification
from alerts.utils import send_emergency_sms
from .tasks import delay_task

def _send_network_notifications_async(user_id, email, phone_number, title, message):
    """
    Asynchronously executes network-bound notifications (Email, SMS, Web Push) in the background.
    We fetch the User model inside the thread context to ensure database session safety.
    """
    # 1. Email via SMTP
    if email:
        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

    # 2. SMS via Twilio API
    if phone_number:
        try:
            send_emergency_sms(phone_number, f"{title}\n{message}")
        except Exception:
            pass

    # 3. Web Push Notification via HTTP WebPush Protocol
    if user_id:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            payload = {
                'head': title,
                'body': message,
                'icon': 'https://i.imgur.com/dZ1Bq4i.png'
            }
            send_user_notification(user=user, payload=payload, ttl=1000)
        except Exception:
            pass

def send_omnichannel_notification(user, title, message):
    """
    Dispatches a notification via multiple channels:
    1. In-App Notification (Database) -> Synchronous/Instant DB write (< 1ms)
    2. Email, SMS, and Web Push -> Asynchronous background thread execution (network latency offloaded)
    """
    # 1. In-App Notification (Synchronous, instant, database integrity)
    try:
        InAppNotification.objects.create(
            user=user,
            title=title,
            message=message
        )
    except Exception:
        pass

    # 2. Dispatch high-latency SMTP / Twilio / WebPush network tasks to background Thread Pool
    email = user.email if user.email else None
    phone_number = user.phone_number if hasattr(user, 'phone_number') and user.phone_number else None
    
    delay_task(
        _send_network_notifications_async,
        user_id=user.pk,
        email=email,
        phone_number=phone_number,
        title=title,
        message=message
    )
