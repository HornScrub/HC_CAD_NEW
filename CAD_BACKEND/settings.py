import os, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-il6+ea&xi3so4$wn^w=fozg0pd(c=y^t6$v^y+56xk!v7x-=v@'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG= True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', 
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg', # Yet Another Swagger Generator - Interactive Swagger UI
    'calls',
    'units',
    'records',
    'incidents',
    'interactions',
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

ROOT_URLCONF = 'CAD_BACKEND.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'CAD_BACKEND.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



# Check if we should use the test database
USE_TEST_DB = os.getenv("USE_TEST_DB", "").strip().lower() in ["true", "1"]
DJANGO_TEST_MODE = "test" in sys.argv

# Default Database (Production/Development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "dispatch_db"),
        "USER": os.getenv("DB_USER", "dispatch_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "whateveryouwant"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
    "persistent_test": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("TEST_DB_NAME", "test_dispatch_db"),
        "USER": os.getenv("TEST_DB_USER", "test_dispatch_user"),
        "PASSWORD": os.getenv("TEST_DB_PASSWORD", "whateveryouwant"),
        "HOST": os.getenv("TEST_DB_HOST", "localhost"),
        "PORT": os.getenv("TEST_DB_PORT", "5432"),
    }
}



# If USE_TEST_DB is set, switch to test database
if USE_TEST_DB or DJANGO_TEST_MODE:
    DATABASES["default"] = DATABASES["persistent_test"]



# Django’s ephemeral test DB override (for unit tests)
if "test" in os.getenv("DJANGO_TEST_MODE", ""):
    DATABASES["default"]["NAME"] = "test_default"


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Adjust based on frontend needs
    "http://your-ai-dispatcher-url.com"
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = True

USE_JWT = os.getenv("USE_JWT", "True") == "True"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ) if USE_JWT else (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ) if USE_JWT else (
        'rest_framework.permissions.AllowAny',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Adjust this number as needed
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debugging: Show active database
if "runserver" in sys.argv and os.environ.get("RUN_MAIN") == "true":
    print(f"⚠️ Switching to Test Database ⚠️" if USE_TEST_DB else "Using Primary Database")
    print(f"Active Database: {DATABASES['default']['NAME']}")
    print(f"USE_TEST_DB: {USE_TEST_DB}")
    print(f"USE JWT: {USE_JWT}")
    print(f"DJANGO_TEST_MODE: {os.getenv('DJANGO_TEST_MODE', 'Not Set')}")

# Import local settings if they exist
try:
    from .settings_local import *
except ImportError:
    pass  # If no local settings, continue normally

