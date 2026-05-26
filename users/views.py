from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from services.decorators import role_required
from .models import User


def login_view(request):
    """Login for Residents only."""
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'STAFF_DISPATCH':
            return redirect('dashboard')
        elif request.user.role == 'STAFF_INVENTORY':
            return redirect('staff_inventory')
        elif request.user.role == 'STAFF_ACCOUNTS':
            return redirect('accounts_dashboard')
        elif request.user.role == 'DRIVER':
            return redirect('driver_app')
        else:
            return redirect('resident_app')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            if user.role != 'RESIDENT':
                messages.error(request, 'This login is for Residents only.')
                return render(request, 'login.html')
            login(request, user)
            return redirect('resident_app')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register_view(request):
    """Self-registration for Residents only."""
    if request.user.is_authenticated:
        return redirect('resident_app')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            role='RESIDENT', phone_number=phone_number, address=address
        )
        login(request, user)
        return redirect('resident_app')

    return render(request, 'register.html')


def driver_login_view(request):
    """Login for Drivers only."""
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role not in ('RESIDENT', 'DRIVER'):
            return redirect('dashboard')
        elif request.user.role == 'DRIVER':
            return redirect('driver_app')
        else:
            return redirect('resident_app')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            if user.role != 'DRIVER':
                messages.error(request, 'This login is for Drivers only.')
                return render(request, 'driver_login.html')
            login(request, user)
            return redirect('driver_app')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'driver_login.html')


def driver_register_view(request):
    """Driver creation — only accessible by existing admins."""
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'Only existing admins can create new driver accounts.')
        return redirect('staff_login')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone_number = request.POST.get('phone_number', '')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'driver_register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'driver_register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            role='DRIVER', phone_number=phone_number
        )
        user.is_staff = False
        user.save()
        messages.success(request, f'Driver account "{username}" created successfully!')
        return redirect('driver_register')

    return render(request, 'driver_register.html')


def staff_login_view(request):
    """Login portal for Admin and Staff only."""
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'STAFF_DISPATCH':
            return redirect('dashboard')
        elif request.user.role == 'STAFF_INVENTORY':
            return redirect('staff_inventory')
        elif request.user.role == 'STAFF_ACCOUNTS':
            return redirect('accounts_dashboard')
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Block residents/drivers from using the staff portal (unless they are superuser)
            if user.role in ('RESIDENT', 'DRIVER') and not user.is_superuser:
                messages.error(request, 'This portal is for staff only. Please use the User Login.')
                return render(request, 'staff_login.html')
            login(request, user)
            if user.is_superuser or user.role == 'STAFF_DISPATCH':
                return redirect('dashboard')
            elif user.role == 'STAFF_ACCOUNTS':
                return redirect('accounts_dashboard')
            else:
                return redirect('staff_inventory')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'staff_login.html')


def staff_create_view(request):
    """Staff account creation — only accessible by existing admins."""
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'Only existing admins can create new staff accounts.')
        return redirect('staff_login')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone_number = request.POST.get('phone_number', '')

        staff_role = request.POST.get('staff_role', 'STAFF_DISPATCH')
        designation = request.POST.get('designation', '')
        salary_str = request.POST.get('salary', '')
        
        salary = None
        if salary_str:
            try:
                salary = float(salary_str)
            except ValueError:
                pass

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'staff_create.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'staff_create.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=staff_role,
            phone_number=phone_number,
            designation=designation,
            salary=salary,
        )
        user.is_staff = False # Explicitly block them from Django DB Admin
        user.save()
        messages.success(request, f'Staff account "{username}" created successfully!')
        return redirect('staff_create')

    return render(request, 'staff_create.html')


def logout_view(request):
    role = getattr(request.user, 'role', None)
    logout(request)
    if role == 'DRIVER':
        return redirect('driver_login')
    elif role in ('ADMIN',) or getattr(request.user, 'is_staff', False):
        return redirect('staff_login')
    return redirect('login')


@role_required(allowed_roles=['STAFF_DISPATCH', 'STAFF_INVENTORY', 'STAFF_ACCOUNTS', 'ADMIN'])
def staff_list_view(request):
    """View to list all staff members and delivery drivers."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Fetch all staff and drivers
    staff_members = User.objects.filter(
        role__in=['STAFF_DISPATCH', 'STAFF_INVENTORY', 'STAFF_ACCOUNTS', 'ADMIN', 'DRIVER']
    ).order_by('role', 'username')
    
    return render(request, 'staff_list.html', {'staff_members': staff_members})
