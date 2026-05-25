import re
import os

views_path = "d:/Work/new_msg/services/views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    my_requests = WaterRequest.objects.filter(resident=request.user).order_by('-created_at')[:5]
    my_notifications = request.user.in_app_notifications.all()
    unread_count = my_notifications.filter(is_read=False).count()

    return render(request, 'resident_app.html', {
        'my_requests': my_requests,
        'my_notifications': my_notifications,
        'unread_count': unread_count,
        'price_per_liter': float(settings.price_per_liter),
        'delivery_fee': float(settings.delivery_fee),
        'urgent_surcharge': float(settings.urgent_surcharge),
        'critical_surcharge': float(settings.critical_surcharge),
    })"""

replacement = """    import json
    my_requests = WaterRequest.objects.filter(resident=request.user).order_by('-created_at')[:20]
    my_notifications = request.user.in_app_notifications.all()
    unread_count = my_notifications.filter(is_read=False).count()

    # Serialize for React
    req_data = [
        {
            'id': r.id,
            'volume_liters': r.volume_liters,
            'priority': r.get_priority_display(),
            'status': r.get_status_display(),
            'status_raw': r.status,
            'cost': float(r.cost),
            'created_at': r.created_at.strftime('%b %d, %H:%M')
        } for r in my_requests
    ]
    
    notif_data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%b %d, %I:%M %p')
        } for n in my_notifications
    ]
    
    initial_data = {
        'user': {
            'username': request.user.username,
            'balance': float(request.user.account_balance),
        },
        'requests': req_data,
        'notifications': notif_data,
        'unread_count': unread_count,
        'pricing': {
            'price_per_liter': float(settings.price_per_liter),
            'delivery_fee': float(settings.delivery_fee),
            'urgent_surcharge': float(settings.urgent_surcharge),
            'critical_surcharge': float(settings.critical_surcharge),
        }
    }

    return render(request, 'react_resident.html', {
        'initial_data_json': json.dumps(initial_data),
        'csrf_token_value': request.META.get('CSRF_COOKIE', ''),
    })"""

content = content.replace(target, replacement)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated views.py to serve React context.")
