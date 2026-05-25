import re
import os

views_path = "d:/Work/new_msg/services/views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    # Drivers only see requests forwarded by inventory, plus what they have already claimed
    from django.db.models import Q
    active_requests = WaterRequest.objects.filter(
        Q(status='FORWARDED') | Q(status='ON_THE_WAY', driver=request.user)
    ).order_by('-created_at')
    
    return render(request, 'driver_app.html', {'active_requests': active_requests})"""

replacement = """    # Drivers only see requests forwarded by inventory, plus what they have already claimed
    from django.db.models import Q
    import json
    active_requests = WaterRequest.objects.filter(
        Q(status='FORWARDED') | Q(status='ON_THE_WAY', driver=request.user)
    ).order_by('-created_at')
    
    req_data = [
        {
            'id': r.id,
            'resident_username': r.resident.username,
            'resident_initial': r.resident.username[0].upper(),
            'volume_liters': r.volume_liters,
            'priority': r.get_priority_display(),
            'status': r.get_status_display(),
            'status_raw': r.status,
            'cost': float(r.cost),
            'created_at': r.created_at.strftime('%b %d, %H:%M')
        } for r in active_requests
    ]
    
    initial_data = {
        'user': {
            'username': request.user.username,
        },
        'active_requests': req_data
    }
    
    return render(request, 'react_driver.html', {
        'initial_data_json': json.dumps(initial_data),
        'csrf_token_value': request.META.get('CSRF_COOKIE', ''),
    })"""

content = content.replace(target, replacement)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated views.py to serve Driver React context.")
