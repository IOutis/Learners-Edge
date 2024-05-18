"""
Django settings for FirstSite project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sclo^!yi3*y^kyty2)fz2u95o7j79%sbqrd7#vxgf+)fx6$4e*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'channels',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
    'register.apps.RegisterConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'notifications',
    'notifications_app.apps.NotificationsAppConfig',
    'django_celery_results',
    'django_celery_beat',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'home.middleware.ThreadLocalMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FirstSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'FirstSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'learners',  # Your database name
        'USER': 'root',  # Your MySQL username
        'PASSWORD': 'mmh13138',  # Your MySQL password
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',  # Default MySQL port
    }
}


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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

#Added Manually
import os
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

ASGI_APPLICATION = 'FirstSite.asgi.application'






from django.core.management.base import BaseCommand
# from home.tasks import check_due_tasks

# class Command(BaseCommand):
#     help = 'Check due tasks and send notifications'

#     def handle(self, *args, **options):
#         check_due_tasks.delay()




CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK="bootstrap5"

LOGIN_REDIRECT_URL="/"
LOGOUT_REDIRECT_URL = "/"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nickcaffery086@gmail.com'
EMAIL_HOST_PASSWORD = 'aonb loih ifrg vccb'
DEFAULT_FROM_EMAIL = 'nickcaffery086@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'nickcaffery086@gmail.com'



#to be removed later 
SECURE_SSL_REDIRECT   = False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False


#celery settings
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER ='json'
# CELERY_TASK_SERIALIZER  =   'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ENABLE_UTC = False

#django-notifications-hq
DJANGO_NOTIFICATIONS_CONFIG = { 'SOFT_DELETE': True}

# Broker Connection Retry
broker_connection_retry_on_startup = True


#celery beat settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'