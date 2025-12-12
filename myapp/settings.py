# myapp/settings.py
from pathlib import Path
import environ
import os

# Initialise django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier .env qui sera créé par AWS
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- CONFIGURATION DES SECRETS (LUS DEPUIS .ENV) ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

# L'ALB agira comme proxy, donc on peut autoriser tous les hôtes ici.
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'storages',  # Ajout pour S3
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

ROOT_URLCONF = 'myapp.urls'

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

# Ton nom de projet est 'myapp'
WSGI_APPLICATION = 'myapp.wsgi.application'


# --- CONFIGURATION AWS (BASE DE DONNÉES & CACHE) ---

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    'default': env.db()
}
DATABASES['default']['OPTIONS'] = {
  'sql_mode': 'STRICT_TRANS_TABLES',
}


# Cache (Redis)
# https://docs.djangoproject.com/en/6.0/ref/settings/#caches
CACHES = {
    "default": env.cache('REDIS_URL')
}


# --- CONFIGURATION S3 POUR LES FICHIERS STATIQUES ---

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')

# Indique à boto3 que la région est Osaka
AWS_S3_REGION_NAME = 'ap-northeast-3'

# Ceci est la ligne la plus importante.
# On dit à django-storages de NE PAS générer d'URL pré-signées.
AWS_QUERYSTRING_AUTH = False

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Les fichiers statiques (CSS, JS) iront dans le dossier "static"
STATICFILES_LOCATION = 'static'
# Les fichiers uploadés par les utilisateurs (media) iront dans le dossier "media"
MEDIAFILES_LOCATION = 'media'

# Configuration pour que django-storages utilise S3 avec les bons sous-dossiers
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": MEDIAFILES_LOCATION,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": STATICFILES_LOCATION,
        },
    },
}

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True