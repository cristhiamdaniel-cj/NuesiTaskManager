from pathlib import Path
import os

# === BASE ===
BASE_DIR = Path(__file__).resolve().parent.parent
FRONT_BASE = os.getenv("FRONT_BASE", "http://localhost:3000")

# === SECURITY ===
SECRET_KEY = 'django-insecure-kzm9r)eo08het9l9-6yf+ei71$ku-asgc0$4kqo-klz2pqvrcx'
DEBUG = True

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1', '192.168.2.29', '10.100.42.36',
    'devops-neusi.ngrok.io', '*'
]

# === CSRF / CORS ===
CSRF_TRUSTED_ORIGINS = [
    'https://devops-neusi.ngrok.io',
    'http://devops-neusi.ngrok.io',
    'http://localhost:8076',
    'http://127.0.0.1:8076',
]

INSTALLED_APPS = [
    # Apps internas
    'backlog',
    'disponibilidad',

    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Integraciones DRF / CORS / Swagger JC
    'rest_framework',
    'corsheaders',
    'drf_spectacular',          # 🧩 nuevo JC
    'drf_spectacular_sidecar',  # 🧩 nuevo JC (activos locales)
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

# === Cookies de desarrollo ===
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# === DRF CONFIG ===
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # ⚙️ Nuevo handler global de errores (JC)
    "EXCEPTION_HANDLER": "backlog.api.exceptions.custom_exception_handler",
    # ⚙️ Integración con drf-spectacular (JC)
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# === Swagger / OpenAPI (JC) ===
SPECTACULAR_SETTINGS = {
    "TITLE": "NEUSI Task Manager API",
    "DESCRIPTION": "Documentación automática de los endpoints del Backlog (Auth, Épicas, Sprints, Tareas, Matriz).",
    "VERSION": "v1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api",  # opcional: agrupa bajo /api
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # carpeta global JC
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

ROOT_URLCONF = 'neusi_tasks.urls'
WSGI_APPLICATION = 'neusi_tasks.wsgi.application'

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === Passwords ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Localización ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "America/Bogota"
USE_TZ = True
USE_I18N = True

# === Archivos estáticos y media ===
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Login redirecciones ===
LOGIN_URL = f"{FRONT_BASE}/login"
LOGIN_REDIRECT_URL = f"{FRONT_BASE}/"
LOGOUT_REDIRECT_URL = f"{FRONT_BASE}/login"
