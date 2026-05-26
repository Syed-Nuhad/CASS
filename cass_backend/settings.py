import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

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
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / os.environ.get('DB_NAME', 'db.sqlite3') if os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3') == 'django.db.backends.sqlite3' else os.environ.get('DB_NAME'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
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

# Email Configuration (Mocked for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@cass-system.com'

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
        'anon': '60/minute',   # Rate limit for unauthenticated scrapers/attackers
        'user': '120/minute',  # Rate limit for authenticated users
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
SESSION_COOKIE_SECURE = True        # Send cookie only over encrypted HTTPS
CSRF_COOKIE_SECURE = True           # Send CSRF cookie only over encrypted HTTPS
SESSION_COOKIE_HTTPONLY = True      # Cookie inaccessible to client JS (prevents XSS leak)
CSRF_COOKIE_HTTPONLY = True        # CSRF token inaccessible to client JS (prevents XSS leak)
SESSION_COOKIE_SAMESITE = 'Strict'  # Mitigate Cross-Site Request Forgery (CSRF)
CSRF_COOKIE_SAMESITE = 'Strict'

# 4. HTTPS Redirect (Will be fully active in production deployment)
SECURE_SSL_REDIRECT = False         # Flip to True on production with an active SSL certificate

# Authentication Routing
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Redis channel layer removed for local testing without Redis.
# Using InMemoryChannelLayer (defined above) instead.
