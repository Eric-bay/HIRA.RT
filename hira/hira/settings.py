import os
from pathlib import Path
from django.core.cache import cache
cache.clear()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ASGI application configuration
ASGI_APPLICATION = 'hira.asgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add compressor finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # Ensure this exists
    'compressor.finders.CompressorFinder',  # Add this
]

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT

# Quick-start development settings
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'channels',
    'jazzmin',
    'tracker',
    'filer',
    'import_export',
    'compressor',  # Keep this one
    'mptt',
    'easy_thumbnails',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hira.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hira.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Email configuration (update with your actual email settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
EMAIL_HOST = 'your-smtp-server.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secret key (generate dynamically in production or use environment variables)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-very-secret-key')

# Jazzmin Admin Interface settings
JAZZMIN_SETTINGS = {
    "site_title": "Hira.RT",
    "site_header": "Hira.RT",
    "site_brand": "Hira.RT",
    "copyright": "EBayejoo",
    "site_logo": "images/logo.png",  # Ensure the logo is available in the 'static/images/' directory
    "welcome_sign": "Welcome to Hira Admin",
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "icons": {
        "tracker.Buyer": "fas fa-users",
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "tracker.EmailModel": "fas fa-envelope",
        "tracker.Requester": "fas fa-users",
        "tracker.Request": "fas fa-file",
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', 'sassc {infile} {outfile}'),
)



