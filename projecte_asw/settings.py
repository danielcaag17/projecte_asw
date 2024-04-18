"""
Django settings for projecte_asw project.

Generated by 'django-admin startproject' using Django 4.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+9)qx*(waqx7qc8ndjhmu#6pr_24jr4=cuj(_e4#n1=*po4ilq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bravo13-36a68ba47d34.herokuapp.com', '127.0.0.1']

# Application definition

SITE_ID = 5

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'api',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'storages'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'api.middleware.AddUserToContextMiddleware'
]

ROOT_URLCONF = 'projecte_asw.urls'

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
                'api.context_processors.usuari_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'projecte_asw.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Obtener la URL de la base de datos de la variable de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

# Configurar las bases de datos
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (css, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = ('static',
                    os.path.join(BASE_DIR, 'static', 'fonts'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# &redirect_uri=login

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_URL = '/accounts/google/login'
LOGIN_REDIRECT_URL = '/login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# S3 settings

AWS_ACCESS_KEY_ID = 'ASIA6GBMBUJHOL74VHNV'
AWS_SECRET_ACCESS_KEY = 'x07gisXcjRtoRlVvTpvSNbxQaHtf97ySeSVi0feu'
AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjELn//////////wEaCXVzLXdlc3QtMiJIMEYCIQC/o1kNjgrLXzqMPX6y1bMzKC9LDMn4sCjGxWoEFM3PmQIhAM5jNA5nAJ61MyWtn6VXmo3LV0MjeoA8ZZ8DnecquKBBKsICCPL//////////wEQABoMOTc1MDQ5OTU3OTY2Igx3OgAEgwEs0IyAq0sqlgLk+yeJ6J8oIn0YnwiqrfFMkY0nJcMl7MQHzG2C9vqVjJqWFqmMnEMAGsqtyT+wWovK2fbgsLaZu+9YtVPLL3ZEAxZy4NanoX54fCNvko14fHspCiDYTAQeTaPLRBdCHHV1tKsZtN/8fMd/1ivZtONs6ZBsIzuNk25r+FzR1R5jn6jz9A6V9S6Nr1JYhkIELcrmSNuqIKbxLTZA1siF3HJrV0urwP690xJk/Rzq0pSkgl6fZd+A+Ogs/pmYrE5plIqxIW9EGchsLbUGwyNycSnolpCbuKfKd3szTjOc8k1axIAejn2c+US7SFJ/I3cuLzDfljv2ujFERXjd+DLl9ePcOBdLgkEIonEhZeMiS2p86JkCHK9yFzDxmYWxBjqcAUEUPHzjb84bQTTISOLhPOXjKw95r2ZM/hrYbQKeCrrpr4ePhBZbmRo43Xp2Edg/ACuNwRiZu+peJpUMnrx9Oz3zFqjcSGG2NkczvbgyGkNPt4YSgYXOmaXxlZG+7aFKfppOnld8epX5kePn9G9/PJw1pUukZFIjOHv4Dk6CQJpf8KCQgnwdw+oRYYawi3YGhvg3V347Lt/q+XaKWA=='
AWS_STORAGE_BUCKET_NAME = 'bravo13-bucket'

# Configura el almacenamiento predeterminado para utilizar S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AVATAR_URL = 's3://bravo13-bucket/avatar/'
COVER_URL = 's3://bravo13-bucket/cover/'
