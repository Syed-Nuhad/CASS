from functools import wraps
from django.shortcuts import redirect

def get_role_redirect_url(user):
    """
    Returns the appropriate redirect view name based on the user's role.
    """
    if user.is_superuser or user.role == 'STAFF_DISPATCH':
        return 'dashboard'
    elif user.role == 'STAFF_INVENTORY':
        return 'staff_inventory'
    elif user.role == 'STAFF_ACCOUNTS':
        return 'accounts_dashboard'
    elif user.role == 'DRIVER':
        return 'driver_app'
    elif user.role == 'RESIDENT':
        return 'resident_app'
    return 'login'

def role_required(allowed_roles):
    """
    Decorator to enforce that the logged-in user belongs to one of the specified allowed_roles.
    If the user has a different authenticated role, they are automatically redirected to 
    their respective dashboard instead of hitting a permission error.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user = request.user
            user_role = getattr(user, 'role', '')
            
            # Superusers are permitted to access dispatch/admin views (like 'dashboard')
            is_allowed = user_role in allowed_roles or (user.is_superuser and 'STAFF_DISPATCH' in allowed_roles)
            
            if not is_allowed:
                dest = get_role_redirect_url(user)
                return redirect(dest)
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
