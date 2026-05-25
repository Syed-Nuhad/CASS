from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyAlert
from users.models import User
from services.utils import send_omnichannel_notification

@login_required
def broadcast_alert_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        
        # Save to database
        alert = EmergencyAlert.objects.create(
            title=title,
            message=message,
            author=request.user
        )

        # Get all residents (Mocking phone numbers for now, or assume they have them)
        residents = User.objects.filter(role='RESIDENT')
        sent_count = 0
        
        for resident in residents:
            try:
                send_omnichannel_notification(
                    user=resident,
                    title=f"CASS ALERT: {title}",
                    message=message
                )
                sent_count += 1
            except Exception:
                pass
                
        alert.sms_sent_count = sent_count
        alert.save()

        messages.success(request, f"Successfully sent omnichannel broadcast to {sent_count} residents!")
        return redirect('dashboard')
    
    return redirect('dashboard')
