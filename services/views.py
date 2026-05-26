from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from .utils import send_omnichannel_notification
from rest_framework import viewsets, permissions
from .models import WaterRequest, MaintenanceRequest, SystemSettings, Inventory, Expense
from .serializers import WaterRequestSerializer, MaintenanceRequestSerializer

@role_required(allowed_roles=['STAFF_DISPATCH'])
def dashboard_view(request):
    water_requests = WaterRequest.objects.all().order_by('-created_at')
    maintenance_requests = MaintenanceRequest.objects.all().order_by('-created_at')
    
    context = {
        'water_requests': water_requests,
        'maintenance_requests': maintenance_requests,
    }
    
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        staff_members = User.objects.filter(
            role__in=['STAFF_DISPATCH', 'STAFF_INVENTORY', 'STAFF_ACCOUNTS', 'ADMIN']
        ).order_by('username')
        context['staff_members'] = staff_members
        
    return render(request, 'dashboard.html', context)

def service_worker_view(request):
    return render(request, 'sw.js', content_type='application/javascript')

@role_required(allowed_roles=['RESIDENT'])
def resident_mobile_view(request):
    settings = SystemSettings.get_settings()

    if request.method == 'POST':
        priority = request.POST.get('priority', 'NORMAL')
        volume = int(request.POST.get('volume', 1000))
        note = request.POST.get('note', '')
        photo = request.FILES.get('photo', None)

        # Cost calculations are now auto-handled by the WaterRequest model on save()
        water_req = WaterRequest.objects.create(
            resident=request.user,
            volume_liters=volume,
            priority=priority,
            status='PENDING',
            note=note,
            photo=photo
        )

        
        # Notify Admins and Inventory Staff
        from django.contrib.auth import get_user_model
        User = get_user_model()
        staff_users = User.objects.filter(role__in=['STAFF_INVENTORY', 'STAFF_DISPATCH'])
        admin_users = User.objects.filter(is_superuser=True)
        
        for u in staff_users:
            send_omnichannel_notification(
                user=u, 
                title='New Water Order! 💧', 
                message=f'{request.user.username} just requested {volume}L of water.'
            )
        for u in admin_users:
            send_omnichannel_notification(
                user=u, 
                title='New Water Order! 💧', 
                message=f'{request.user.username} just requested {volume}L of water.'
            )
            
        return redirect('resident_app')

    import json
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
    
    logo_url = '/static/CASS_logo.png'
    if settings and settings.branding_logo:
        logo_url = settings.branding_logo.url

    initial_data = {
        'user': {
            'username': request.user.username,
            'balance': float(request.user.account_balance),
            'logo_url': logo_url,
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
    })

@role_required(allowed_roles=['DRIVER'])
def driver_mobile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        req_id = request.POST.get('request_id')
        try:
            water_req = WaterRequest.objects.get(id=req_id)
            if action == 'claim' and water_req.status == 'FORWARDED':
                water_req.driver = request.user
                water_req.status = 'ON_THE_WAY'
                water_req.save()
            elif action == 'deliver' and water_req.status == 'ON_THE_WAY' and water_req.driver == request.user:
                water_req.status = 'DELIVERED'
                water_req.save()
                
                # Auto-Billing: Update resident's balance using the saved request cost
                resident = water_req.resident
                resident.account_balance = float(resident.account_balance) + float(water_req.cost)
                resident.save()
                
                # Inventory Deduction
                inventory = Inventory.get_inventory()
                inventory.total_water_liters -= water_req.volume_liters
                inventory.save()
                
                # Send omnichannel notification to the resident
                send_omnichannel_notification(
                    user=resident,
                    title='Delivery Complete! 💧',
                    message=f'Your water delivery ({water_req.volume_liters}L) has arrived. ${water_req.cost} was added to your bill.'
                )
                
        except WaterRequest.DoesNotExist:
            pass
        return redirect('driver_app')

    # Drivers only see requests forwarded by inventory, plus what they have already claimed
    from django.db.models import Q
    import json
    active_requests = WaterRequest.objects.filter(
        Q(status='FORWARDED') | Q(status='ON_THE_WAY', driver=request.user)
    ).order_by('-created_at')
    
    req_data = [
        {
            'id': r.id,
            'resident_username': r.resident.username,
            'resident_address': r.resident.address or 'No address provided',
            'resident_initial': r.resident.username[0].upper(),
            'volume_liters': r.volume_liters,
            'priority': r.get_priority_display(),
            'status': r.get_status_display(),
            'status_raw': r.status,
            'cost': float(r.cost),
            'created_at': r.created_at.strftime('%b %d, %H:%M')
        } for r in active_requests
    ]
    
    logo_url = '/static/CASS_logo.png'
    try:
        from services.models import SystemSettings
        active_settings = SystemSettings.objects.filter(is_active=True).first()
        if active_settings and active_settings.branding_logo:
            logo_url = active_settings.branding_logo.url
    except Exception:
        pass

    initial_data = {
        'user': {
            'username': request.user.username,
            'logo_url': logo_url,
        },
        'active_requests': req_data
    }
    
    return render(request, 'react_driver.html', {
        'initial_data_json': json.dumps(initial_data),
        'csrf_token_value': request.META.get('CSRF_COOKIE', ''),
    })

@role_required(allowed_roles=['DRIVER'])
def driver_order_detail_view(request, pk):
    try:
        req = WaterRequest.objects.get(id=pk)
    except WaterRequest.DoesNotExist:
        return redirect('driver_app')
        
    return render(request, 'driver_order_detail.html', {'req': req})

@role_required(allowed_roles=['STAFF_INVENTORY'])
def staff_inventory_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        req_id = request.POST.get('request_id')
        if action == 'forward':
            try:
                water_req = WaterRequest.objects.get(id=req_id, status='PENDING')
                water_req.status = 'FORWARDED'
                water_req.save()
                
                # Notify the resident that the order was sent for delivery
                send_omnichannel_notification(
                    user=water_req.resident,
                    title='Order Forwarded 🚚',
                    message='Your order has been sent for delivery.'
                )
                
            except WaterRequest.DoesNotExist:
                pass
        return redirect('staff_inventory')

    inventory = Inventory.get_inventory()
    pending_requests = WaterRequest.objects.filter(status='PENDING').order_by('created_at')
    
    return render(request, 'staff_inventory.html', {
        'inventory': inventory,
        'pending_requests': pending_requests
    })

@role_required(allowed_roles=['STAFF_ACCOUNTS'])
def accounts_dashboard_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        if amount and description:
            try:
                Expense.objects.create(amount=float(amount), description=description)
            except ValueError:
                pass
        return redirect('accounts_dashboard')

    from django.utils import timezone
    from django.db.models import Sum
    from decimal import Decimal
    import calendar
    
    now = timezone.now()
    
    # Income (DELIVERED water requests this month)
    monthly_income = WaterRequest.objects.filter(
        status='DELIVERED',
        updated_at__year=now.year,
        updated_at__month=now.month
    ).aggregate(total=Sum('cost'))['total'] or Decimal('0.00')
    
    # Expenses this month
    monthly_expenses = Expense.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    monthly_profit = monthly_income - monthly_expenses
    
    recent_income = WaterRequest.objects.filter(status='DELIVERED').order_by('-updated_at')[:20]
    recent_expenses = Expense.objects.all().order_by('-date')[:20]
    
    annual_data = []
    for month in range(1, 13):
        m_income = WaterRequest.objects.filter(
            status='DELIVERED', updated_at__year=now.year, updated_at__month=month
        ).aggregate(total=Sum('cost'))['total'] or Decimal('0.00')
        
        m_expense = Expense.objects.filter(
            date__year=now.year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        annual_data.append({
            'month': calendar.month_name[month],
            'income': m_income,
            'expense': m_expense,
            'profit': m_income - m_expense
        })

    annual_total_income = sum(item['income'] for item in annual_data)
    annual_total_expense = sum(item['expense'] for item in annual_data)
    annual_total_profit = sum(item['profit'] for item in annual_data)

    # Fetch staff members for the payroll directory
    from django.contrib.auth import get_user_model
    User = get_user_model()
    staff_members = User.objects.filter(
        role__in=['STAFF_DISPATCH', 'STAFF_INVENTORY', 'STAFF_ACCOUNTS', 'ADMIN']
    ).order_by('username')
    
    total_payroll = sum(s.salary for s in staff_members if s.salary)

    context = {
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_profit': monthly_profit,
        'recent_income': recent_income,
        'recent_expenses': recent_expenses,
        'annual_data': annual_data,
        'annual_total_income': annual_total_income,
        'annual_total_expense': annual_total_expense,
        'annual_total_profit': annual_total_profit,
        'current_year': now.year,
        'current_month_name': calendar.month_name[now.month],
        'staff_members': staff_members,
        'total_payroll': total_payroll,
    }
    return render(request, 'accounts_dashboard.html', context)

from django.http import JsonResponse
@login_required
def mark_notifications_read_view(request):
    if request.method == 'POST':
        request.user.in_app_notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'}, status=400)

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

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

@login_required
def export_financial_pdf_view(request):
    if request.user.role != 'STAFF_ACCOUNTS':
        return HttpResponse('Unauthorized: Only accountants are authorized.', status=403)

    from django.utils import timezone
    from django.db.models import Sum
    from decimal import Decimal
    import calendar
    import io

    now = timezone.now()
    
    monthly_income = WaterRequest.objects.filter(
        status='DELIVERED', updated_at__year=now.year, updated_at__month=now.month
    ).aggregate(total=Sum('cost'))['total'] or Decimal('0.00')
    
    monthly_expenses = Expense.objects.filter(
        date__year=now.year, date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    monthly_profit = monthly_income - monthly_expenses
    
    annual_data = []
    for month in range(1, 13):
        m_income = WaterRequest.objects.filter(
            status='DELIVERED', updated_at__year=now.year, updated_at__month=month
        ).aggregate(total=Sum('cost'))['total'] or Decimal('0.00')
        m_expense = Expense.objects.filter(
            date__year=now.year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        annual_data.append({
            'month': calendar.month_name[month],
            'income': m_income,
            'expense': m_expense,
            'profit': m_income - m_expense
        })
        
    annual_total_income = sum(item['income'] for item in annual_data)
    annual_total_expense = sum(item['expense'] for item in annual_data)
    annual_total_profit = sum(item['profit'] for item in annual_data)
        
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    settings = SystemSettings.get_settings()
    if settings and settings.branding_logo:
        try:
            logo_path = settings.branding_logo.path
            img = ImageReader(logo_path)
            p.drawImage(img, 50, height - 100, width=100, height=50, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            pass
            
    p.setFont("Helvetica-Bold", 18)
    p.drawString(160, height - 70, f"Financial Accounts Report - {now.year}")
    
    if settings:
        p.setFont("Helvetica", 10)
        text_y = height - 85
        if settings.company_address:
            p.drawString(160, text_y, settings.company_address)
            text_y -= 12
        contact_str = ""
        if settings.company_email:
            contact_str += f"Email: {settings.company_email}   "
        if settings.company_phone:
            contact_str += f"Phone: {settings.company_phone}"
        if contact_str:
            p.drawString(160, text_y, contact_str.strip())
    
    report_type = request.GET.get('type', 'monthly')

    if report_type == 'monthly':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, f"{calendar.month_name[now.month]} Summary")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 160, f"Total Income: ${monthly_income}")
        p.drawString(50, height - 180, f"Total Expenses: ${monthly_expenses}")
        p.drawString(50, height - 200, f"Net Profit: ${monthly_profit}")
        
        expenses_list = Expense.objects.filter(date__year=now.year, date__month=now.month).order_by('-date')
        income_list = WaterRequest.objects.filter(status='DELIVERED', updated_at__year=now.year, updated_at__month=now.month).order_by('-updated_at')
        
        y = height - 240
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Company Expenses")
        
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Description")
        p.drawString(250, y, "Date")
        p.drawString(400, y, "Amount")
        
        y -= 20
        p.setFont("Helvetica", 10)
        if not expenses_list:
            p.drawString(50, y, "No expenses recorded this month.")
            y -= 20
        else:
            for exp in expenses_list:
                if y < 50:
                    p.showPage()
                    y = height - 50
                p.drawString(50, y, exp.description[:40])
                p.drawString(250, y, exp.date.strftime("%b %d, %Y"))
                p.drawString(400, y, f"-${exp.amount}")
                y -= 20
        
        y -= 20
        if y < 100:
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Delivery Revenue")
        
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Order ID")
        p.drawString(250, y, "Date/Time")
        p.drawString(400, y, "Amount")
        
        y -= 20
        p.setFont("Helvetica", 10)
        if not income_list:
            p.drawString(50, y, "No revenue recorded this month.")
            y -= 20
        else:
            for inc in income_list:
                if y < 50:
                    p.showPage()
                    y = height - 50
                p.drawString(50, y, f"#{inc.id:04d}")
                p.drawString(250, y, inc.updated_at.strftime("%b %d, %H:%M"))
                p.drawString(400, y, f"+${inc.cost}")
                y -= 20
    elif report_type == 'annual':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, "Annual Breakdown")
        
        y = height - 170
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Month")
        p.drawString(150, y, "Income")
        p.drawString(250, y, "Expenses")
        p.drawString(350, y, "Profit")
        
        y -= 20
        p.setFont("Helvetica", 10)
        for row in annual_data:
            if y < 50:
                p.showPage()
                y = height - 50
            
            p.drawString(50, y, row['month'])
            p.drawString(150, y, f"${row['income']}")
            p.drawString(250, y, f"${row['expense']}")
            p.drawString(350, y, f"${row['profit']}")
            y -= 20
            
        y -= 10
        if y < 50:
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Grand Total")
        p.drawString(150, y, f"${annual_total_income}")
        p.drawString(250, y, f"${annual_total_expense}")
        p.drawString(350, y, f"${annual_total_profit}")
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_report.pdf"'
    return response
