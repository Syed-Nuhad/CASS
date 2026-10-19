import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Use PyMySQL as a fallback for MySQLdb on cPanel
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-development-only-!!!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', '*').split(',') if host.strip()]

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'axes',
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'webpush',
    
    # Local apps
    'users',
    'services',
    'alerts',
]

MIDDLEWARE = [
    'services.middleware.DynamicSecurityBypassMiddleware',
    'services.middleware.HoneypotMiddleware',
    'services.middleware.ApplicationWAFMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'services.middleware.OriginLockdownMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'services.middleware.SessionTimeoutMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'services.middleware.IPSessionLockMiddleware',
    'services.middleware.SecurityHeadersMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# AXES Configuration
AXES_ENABLED = False
AXES_FAILURE_LIMIT = 50
AXES_COOLOFF_TIME = 1  # 1 hour
AXES_LOCKOUT_TEMPLATE = None # will return 403 by default
AXES_RESET_ON_SUCCESS = True
AXES_NEVER_LOCKOUT_WHITELIST = True
AXES_IP_WHITELIST = ['127.0.0.1', 'localhost', '::1']

ROOT_URLCONF = 'cass_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'services.context_processors.system_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'cass_backend.wsgi.application'
ASGI_APPLICATION = 'cass_backend.asgi.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / os.environ.get('DB_NAME', 'db.sqlite3') if os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3') == 'django.db.backends.sqlite3' else os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage configuration for compressed & cached static files (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email Configuration (Supports Brevo SMTP or console fallback)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp-relay.brevo.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
else:
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@cass.mentosh.top')

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": os.environ.get("VAPID_PUBLIC_KEY", "BBEb2fP6rP-O44K4wFz_Bf79tO70Y4bN9hPZg6oWcPxO4-vO_cZ1qD24YvIIf0aD_v4Mv5s8lY_E4f2-tA4I1J4"),
    "VAPID_PRIVATE_KEY": os.environ.get("VAPID_PRIVATE_KEY", "a-fake-vapid-private-key-for-development"),
    "VAPID_ADMIN_EMAIL": os.environ.get("VAPID_ADMIN_EMAIL", "admin@example.com")
}

ADMIN_URL_PATH = os.environ.get('ADMIN_URL_PATH', 'Fmp2Il70IF8zjAUr3_d0O/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',   # Rate limit for unauthenticated scrapers/attackers
        'user': '100/minute',  # Rate limit for authenticated users
    }
}

# BANK-GRADE SECURITY HARDENING
# ----------------------------------------------------------------------
# 1. HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year (Force browsers to ONLY load via HTTPS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 2. Browser Vulnerability & Content Security Protections
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-type sniffing attacks
X_FRAME_OPTIONS = 'DENY'            # Prevent Clickjacking (disallow frames entirely)

# 3. Session & CSRF Cookie Hardening (Encrypted/Inaccessible to JS)
SESSION_COOKIE_SECURE = not DEBUG        # Send cookie only over encrypted HTTPS
CSRF_COOKIE_SECURE = not DEBUG           # Send CSRF cookie only over encrypted HTTPS
SESSION_COOKIE_HTTPONLY = True      # Cookie inaccessible to client JS (prevents XSS leak)
CSRF_COOKIE_HTTPONLY = True        # CSRF token inaccessible to client JS (prevents XSS leak)
SESSION_COOKIE_SAMESITE = 'Lax'     # Mitigate Cross-Site Request Forgery (CSRF)
CSRF_COOKIE_SAMESITE = 'Lax'

# 4. HTTPS Redirect (Will be fully active in production deployment)
SECURE_SSL_REDIRECT = False         # Flip to True on production with an active SSL certificate

# 5. Trusted Origins for CSRF verification (required for cPanel HTTPS)
CSRF_TRUSTED_ORIGINS = [
    'https://cass.mentosh.top',
    'http://cass.mentosh.top',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Authentication Routing
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Redis channel layer removed for local testing without Redis.
# Using InMemoryChannelLayer (defined above) instead.
