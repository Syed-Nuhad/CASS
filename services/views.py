from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from webpush import send_user_notification
from rest_framework import viewsets, permissions
from .models import WaterRequest, MaintenanceRequest
from .serializers import WaterRequestSerializer, MaintenanceRequestSerializer

@login_required(login_url='/admin/login/')
def dashboard_view(request):
    water_requests = WaterRequest.objects.all().order_by('-created_at')
    maintenance_requests = MaintenanceRequest.objects.all().order_by('-created_at')
    
    context = {
        'water_requests': water_requests,
        'maintenance_requests': maintenance_requests,
    }
    return render(request, 'dashboard.html', context)

def service_worker_view(request):
    return render(request, 'sw.js', content_type='application/javascript')

@login_required(login_url='/admin/login/')
def resident_mobile_view(request):
    if request.method == 'POST':
        priority = request.POST.get('priority', 'NORMAL')
        volume = request.POST.get('volume', 1000)
        WaterRequest.objects.create(
            resident=request.user,
            volume_liters=volume,
            priority=priority,
            status='PENDING'
        )
        return redirect('resident_app')
        
    my_requests = WaterRequest.objects.filter(resident=request.user).order_by('-created_at')[:5]
    return render(request, 'resident_app.html', {'my_requests': my_requests})

@login_required(login_url='/admin/login/')
def driver_mobile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        req_id = request.POST.get('request_id')
        try:
            water_req = WaterRequest.objects.get(id=req_id)
            if action == 'claim' and water_req.status == 'PENDING':
                water_req.driver = request.user
                water_req.status = 'ON_THE_WAY'
                water_req.save()
            elif action == 'deliver' and water_req.status == 'ON_THE_WAY' and water_req.driver == request.user:
                water_req.status = 'DELIVERED'
                water_req.save()
                
                # Auto-Billing: Calculate cost and update resident's balance
                PRICE_PER_LITER = 0.05
                cost = float(water_req.volume_liters) * PRICE_PER_LITER
                resident = water_req.resident
                # Add the cost to their outstanding balance
                resident.account_balance = float(resident.account_balance) + cost
                resident.save()
                
                # Send Web Push Notification to the resident
                payload = {
                    'head': 'Delivery Complete! 💧',
                    'body': f'Your water delivery ({water_req.volume_liters}L) has arrived. ${cost:.2f} was added to your bill.',
                    'icon': 'https://i.imgur.com/dZ1Bq4i.png'
                }
                send_user_notification(user=resident, payload=payload, ttl=1000)
                
        except WaterRequest.DoesNotExist:
            pass
        return redirect('driver_app')

    # Show pending requests and requests claimed by this driver
    from django.db.models import Q
    active_requests = WaterRequest.objects.filter(
        Q(status='PENDING') | Q(status='ON_THE_WAY', driver=request.user)
    ).order_by('-created_at')
    
    return render(request, 'driver_app.html', {'active_requests': active_requests})

class WaterRequestViewSet(viewsets.ModelViewSet):
    queryset = WaterRequest.objects.all().order_by('-created_at')
    serializer_class = WaterRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the resident
        serializer.save(resident=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'RESIDENT':
            # Residents only see their own requests
            return self.queryset.filter(resident=user)
        elif user.role == 'DRIVER':
            # Drivers see all pending requests + requests assigned to them
            return self.queryset.filter(status='PENDING') | self.queryset.filter(driver=user)
        # Admins see everything
        return self.queryset

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all().order_by('-created_at')
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user)
