"""
Django settings for axf project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a9ir*f810p2n56@4wzmco5ar5(j3mij)wh$xol9x@#hi85wmn0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App.apps.AppConfig',
    "django_celery_results",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.middleware.LoginMiddleware',
]

ROOT_URLCONF = 'axf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ]
        ,
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

WSGI_APPLICATION = 'axf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
CACHES = {
    "default": {
            "BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": "redis://xuaman.top:6379/1",
                            "OPTIONS": {
                                        "CLIENT_CLASS": "django_redis.client.DefaultClient",
                                                    "PICKLE_VERSION": -1,
                                                            }
                                                                }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'axf',
        'USER': 'root',
        'PASSWORD': 'gundan..0',
        'HOST': 'localhost',
        'PORT': 3306,

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static"),
]
MEDIA_ROOT = os.path.join(BASE_DIR, "static/uploads")

MEDIA_KEY_PREFIX="/static/uploads/"

INTERNAL_IPS = ('127.0.0.1', 'localhost', '10.0.122.179')

EMAIL_HOST = 'smtp.163.com'

EMAIL_USE_SSL = True

EMAIL_PORT = 465

EMAIL_HOST_USER = 'xam0415@163.com'

EMAIL_HOST_PASSWORD = 'xam0415'

SERVER_HOST = 'xuaman.top'

SERVER_PORT = '9000'



ALIPAY_APPID = "2016092100561216"

APP_PRIVATE_KEY = open(os.path.join(BASE_DIR, 'alipay_config/app_rsa_private_key.pem'), 'r').read()

ALIPAY_PUBLIC_KEY = open(os.path.join(BASE_DIR, 'alipay_config/alipay_rsa_public_key.pem'), 'r').read()


CELERY_BROKER_URL = 'redis://xuaman.top:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
