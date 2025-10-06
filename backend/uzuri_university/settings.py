import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# --- DRF Throttling ---
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    }
}
# --- Caching ---
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
# During test runs use local memory cache to avoid requiring Redis.
if 'test' in sys.argv or os.environ.get('PYTEST_CURRENT_TEST'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-test-cache'
        }
    }
    # Keep migrations enabled; tests need a consistent migration graph.
    # Keep migrations enabled; tests need a consistent migration graph.
# --- Internationalization ---
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('sw', 'Swahili'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
# --- Security Settings ---
# Allow disabling strict HTTPS enforcement in development by setting DJANGO_DEBUG=True
# If DJANGO_DEBUG == 'True' then these security flags will be relaxed for local testing.
_DJANGO_DEBUG_ENV = os.environ.get('DJANGO_DEBUG', 'False')
SECURE_SSL_REDIRECT = False if _DJANGO_DEBUG_ENV == 'True' else True
SESSION_COOKIE_SECURE = False if _DJANGO_DEBUG_ENV == 'True' else True
CSRF_COOKIE_SECURE = False if _DJANGO_DEBUG_ENV == 'True' else True
SECURE_HSTS_SECONDS = 0 if _DJANGO_DEBUG_ENV == 'True' else 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = False if _DJANGO_DEBUG_ENV == 'True' else True
SECURE_HSTS_PRELOAD = False if _DJANGO_DEBUG_ENV == 'True' else True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGIN_WHITELIST', '').split(',') if os.environ.get('CORS_ORIGIN_WHITELIST') else []
# --- Imports ---
# (core stdlib imports are declared at the top of this file; avoid duplicate imports)
# Google Calendar API credentials
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
# Outlook Calendar API credentials
OUTLOOK_CLIENT_ID = os.environ.get('OUTLOOK_CLIENT_ID', 'your-outlook-client-id')
OUTLOOK_CLIENT_SECRET = os.environ.get('OUTLOOK_CLIENT_SECRET', 'your-outlook-client-secret')
# Africa's Talking SMS credentials
AFRICASTALKING_USERNAME = os.environ.get('AFRICASTALKING_USERNAME', '')
AFRICASTALKING_API_KEY = os.environ.get('AFRICASTALKING_API_KEY', '')
# Suppress drf-yasg Swagger renderer deprecation warning
SWAGGER_USE_COMPAT_RENDERERS = False
# --- Logging & Error Monitoring ---
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
except ImportError:
    sentry_sdk = None
    DjangoIntegration = None

# Sentry configuration (replace with your DSN)
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
# --- Payment Gateway & SMS Provider Production Credentials ---
MPESA_ENV = 'production'  # or 'sandbox'
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', '')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', '')
# Stripe settings
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE', '')
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', '')
MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL', '')
MPESA_WEBHOOK_SECRET = os.environ.get('MPESA_WEBHOOK_SECRET', '')
SMS_API_KEY = os.environ.get('SMS_API_KEY', '')
SMS_SENDER = os.environ.get('SMS_SENDER', 'sandbox')
SMS_URL = os.environ.get('SMS_URL', 'https://api.sandbox.africastalking.com/version1/messaging')
# Celery Beat Schedule
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'auto-archive-notifications': {
        'task': 'my_profile.tasks.auto_archive_notifications',
        'schedule': crontab(hour=0, minute=0),  # daily at midnight
    },
    'send-overdue-reminders': {
        'task': 'fees.tasks.send_overdue_reminders_task',
        'schedule': crontab(hour=8, minute=0),  # daily at 8am
    },
    'auto-generate-invoices': {
        'task': 'fees.tasks.auto_generate_invoices_task',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),  # monthly
    },
    'auto-clearance': {
        'task': 'fees.tasks.auto_clearance_task',
        'schedule': crontab(hour=3, minute=0),  # daily at 3am
    },
    'mark-unpaid-hostel-invoices-overdue': {
        'task': 'hostel.views.mark_unpaid_hostel_invoices_overdue',
        'schedule': crontab(hour=7, minute=0),  # daily at 7am
    },
    'send-hostel-fee-reminders': {
        'task': 'hostel.views.send_hostel_fee_reminders',
        'schedule': crontab(hour=12, minute=0),  # daily at noon
    },
    'auto-generate-exam-cards': {
        'task': 'exam_card.tasks.auto_generate_exam_cards',
        'schedule': crontab(hour=1, minute=0),  # daily at 1am
    },
    'send-exam-card-notifications': {
        'task': 'exam_card.tasks.send_exam_card_notifications',
        'schedule': crontab(hour=9, minute=0),  # daily at 9am
    },
}
"""
Django settings for uzuri_university project.

Generated by 'django-admin startproject' using Django 5.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-9k)-f4iy3fb1$*t5hupfx7ou9vs^fob)cj$s7cpu+whwp*90m2')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG can be toggled for local development by setting the DJANGO_DEBUG environment variable to 'True'
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost', '127.0.0.1']  # Replace with your actual domain(s)

# Security settings
# Respect DEBUG so local development doesn't force HTTPS or set secure-only cookies.
# In production (DEBUG=False) these should be True / strict values.
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# HSTS: zero during development, long-lived in production
SECURE_HSTS_SECONDS = 0 if DEBUG else 31536000
# Include subdomains/preload only in production
SECURE_HSTS_INCLUDE_SUBDOMAINS = False if DEBUG else True
SECURE_HSTS_PRELOAD = False if DEBUG else True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS settings (if using APIs cross-domain)
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]


# Media files for QR/barcode images
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# When running tests, relax strict security settings to avoid HTTPS redirects and
# DisallowedHost errors caused by the test client (which uses 'testserver').
if 'test' in sys.argv or os.environ.get('PYTEST_CURRENT_TEST'):
    DEBUG = True
    # Avoid redirecting to HTTPS during tests which converts POST->GET on follow
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    # Allow the Django test client's default host
    ALLOWED_HOSTS = ALLOWED_HOSTS + ['testserver', 'localhost']
    # Disable MFA enforcement during tests so middleware doesn't block APIClient.force_authenticate
    MFA_ENABLED = False
    # Note: do not change REST_FRAMEWORK here; keep test-time overrides minimal.

# Exam card expiry (days)
EXAM_CARD_EXPIRY_DAYS = 30

# Branding assets and PDF template settings for exam card
EXAM_CARD_LOGO_PATH = BASE_DIR / 'branding' / 'logo.png'
EXAM_CARD_SIGNATURE_PATH = BASE_DIR / 'branding' / 'signature.png'
EXAM_CARD_STAMP_PATH = BASE_DIR / 'branding' / 'stamp.png'
EXAM_CARD_PDF_LAYOUT = 'default'  # Can be customized via admin
EXAM_CARD_PDF_FOOTER = 'This card is valid for the current exam period only.'

# PDF generation library (install e.g. reportlab or weasyprint)
# Example: pip install reportlab

# Security enhancements for exam card
EXAM_CARD_WATERMARK_TEXT = 'Uzuri University Official'
EXAM_CARD_QR_ENCRYPTION_KEY = 'replace-with-secure-key'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'fees',
    'my_profile',
    'hostel',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'rest_auth',
    'rest_framework',
    'rest_framework_simplejwt',
    'unit_registration',
    'exam_card',
    'provisional_results',
    'final_results',
    'lecturer_evaluation',
    'disciplinary',
    'academic_leave',
    'timetable',
    'attachments',
    'graduation',
    'clearance',
    'payments',
    'uzuri_calendar',
    'emasomo',
    'notifications',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'core.middleware_security.AuditLogMiddleware',
    'core.middleware_security.MFAEnforcementMiddleware',
    'core.middleware_security.EncryptionHeadersMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS configuration for local frontend development
# Allow specifying CORS origins via env or default to common dev ports
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
CORS_ORIGIN_ALLOW_ALL = os.environ.get('CORS_ORIGIN_ALLOW_ALL', 'False') in ('True', 'true', '1')

# REST Framework global settings: JWT auth, pagination, filters
REST_FRAMEWORK.update({
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
})

# If running tests, make sure the debug middleware is present so we capture
# PermissionDenied tracebacks for diagnostics. The earlier test-time block
# toggles DEBUG/MFA; this placement ensures MIDDLEWARE is defined before we
# attempt to mutate it.
if 'test' in sys.argv or os.environ.get('PYTEST_CURRENT_TEST'):
    # No test-only middleware inserted.
    pass

ROOT_URLCONF = 'uzuri_university.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Channels
ASGI_APPLICATION = 'uzuri_university.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# During tests use an in-memory channel layer to avoid requiring a running
# Redis instance and to silence noisy connection refused logs from tests.
if 'test' in sys.argv or os.environ.get('PYTEST_CURRENT_TEST'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        }
    }

WSGI_APPLICATION = 'uzuri_university.wsgi.application'
# Celery settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
    # Add more languages as needed
]
LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'core.CustomUser'

# Django Allauth settings for OAuth2
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'microsoft': {
        'SCOPE': ['User.Read'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
}


# Django OTP settings (basic)
OTP_TOTP_ISSUER = 'Uzuri University'

# Add finance_registration and token auth to installed apps
# The project previously referenced many optional apps here. Those
# apps are not present in this repository and were only declared in
# settings; to avoid import errors during startup we only register
# present apps. Add back any removed apps here if you actually add
# their packages to the codebase.
INSTALLED_APPS += [
    'finance_registration',
    'rest_framework.authtoken',
]

# Django REST Framework & JWT settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
        'login': '5/minute',
    },
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
