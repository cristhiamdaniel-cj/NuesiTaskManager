from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FRONT_BASE = os.getenv("FRONT_BASE", "http://localhost:3000")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kzm9r)eo08het9l9-6yf+ei71$ku-asgc0$4kqo-klz2pqvrcx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.2.29', '10.100.42.36', 'devops-neusi.ngrok.io', '*']

# CSRF Configuration for ngrok
CSRF_TRUSTED_ORIGINS = [
    'https://devops-neusi.ngrok.io',
    'http://devops-neusi.ngrok.io',
    'http://localhost:8076',
    'http://127.0.0.1:8076',
    
]
# Application definition

INSTALLED_APPS = [
    'backlog',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'disponibilidad',

    #Integracion DRF+CORS /JC
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',     # integracion CORS/JC
    'django.middleware.common.CommonMiddleware', # integracion CORS/JC
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',


    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# --- CORS/CSRF para Next.js /JC ---
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://192.168.2.29:3000',
    'http://10.100.42.36:3000',
    'https://devops-neusi.ngrok.io',
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS += [
    'https://devops-neusi.ngrok.io',
    'http://devops-neusi.ngrok.io',
    # backends
    'http://localhost:8076',
    'http://127.0.0.1:8076',
    'http://192.168.2.29:8076',
    'http://10.100.42.36:8076',
    # frontends
    'http://localhost:3000',
    'http://192.168.2.29:3000',
    'http://10.100.42.36:3000',
]

# Cookies de dev (ajusta a True si usas HTTPS)/JC---
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE    = 'Lax'
SESSION_COOKIE_SECURE   = False
CSRF_COOKIE_SECURE      = False

#  DRF por defecto: sesiones/JC ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "EXCEPTION_HANDLER": ["backlog.api.exceptions.custom_exception_handler"
    ],
}

ROOT_URLCONF = 'neusi_tasks.urls'
"""
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
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # 👈 aquí añadimos la carpeta global
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

WSGI_APPLICATION = 'neusi_tasks.wsgi.application'


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
# settings.py
TIME_ZONE = "America/Bogota"
USE_TZ = True


USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = f"{FRONT_BASE}/login"
LOGIN_REDIRECT_URL = f"{FRONT_BASE}/"      
LOGOUT_REDIRECT_URL = f"{FRONT_BASE}/login"
import os

# Archivos subidos (media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
