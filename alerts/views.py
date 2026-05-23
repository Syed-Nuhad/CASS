from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EmergencyAlert
from .utils import send_emergency_sms
from users.models import User

@login_required(login_url='/admin/login/')
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
            # We assume a dummy phone number since we didn't add phone to User model
            dummy_phone = "+15550000000"
            success = send_emergency_sms(dummy_phone, f"CASS ALERT: {title}\\n{message}")
            if success:
                sent_count += 1
                
        alert.sms_sent_count = sent_count
        alert.save()

        return redirect('dashboard')
    
    return redirect('dashboard')
