
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y$xq3tg(-pqfgp7im-62lh1*-i@kt87e%pwhe6)w3^u=kz5^xe'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []

DEBUG = True
ALLOWED_HOSTS = ['*']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'ckeditor',
    'taggit',
    'siteweb.apps.SitewebConfig',
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
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

ROOT_URLCONF = 'monsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'monsite.wsgi.application'
# ASGI_APPLICATION = 'monsite.asgi.application'
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],  # adresse du serveur Redis
#         },
#     },
# }


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'bangri',
        'USER':'trebmal',
        'PASSWORD':'manulove',
        'HOST':'localhost',
        'PORT':'4444',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Chemin absolu vers le répertoire de destination pour les fichiers statiques collectés
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#Configuration pour le backend de messagerie de production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'bikoyemmanuel531@gmail.com'
EMAIL_HOST_PASSWORD = 'ywvm uols wmhe jymi'
#DEFAULT_FROM_EMAIL = 'bangwenbikoy@gmail.com'

# Configuration Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL de connexion à Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Sauvegarder les résultats des tâches dans Redis
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-newsletter-every-month': {
        'task': 'monsite.tasks.scheduled_newsletter',
        'schedule': crontab(day_of_month=1, hour=10, minute=0),  # Planifié le 1er jour de chaque mois à 10h
    },
}

# settings.py
ORANGE_MONEY_API_KEY = 'votre_clé_API'
ORANGE_MONEY_SECRET_KEY = 'votre_clé_secrète'
ORANGE_MONEY_CALLBACK_URL = 'https://votre-domaine.com/callback/'
ORANGE_MONEY_MERCHANT_ACCOUNT = 'votre_compte_merchant'

