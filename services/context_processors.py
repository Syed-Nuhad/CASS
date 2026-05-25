from .models import SystemSettings

def system_settings(request):
    """
    Context processor to make global system settings (like the branding logo)
    available to all templates.
    """
    settings = SystemSettings.get_settings()
    return {
        'system_settings': settings
    }
