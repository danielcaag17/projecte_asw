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
    'kbin',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'storages',
    "api.apps.ApiConfig",
    'corsheaders',
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
    'kbin.middleware.AddUserToContextMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # Permitir solicitudes de cualquier origen
CORS_ALLOW_HEADERS = ["keyword","Authorization"]

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
                'kbin.context_processors.usuari_context_processor',
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

AWS_ACCESS_KEY_ID = 'ASIA6GBMBUJHMLKRRXF2'
AWS_SECRET_ACCESS_KEY = 'KmhoLav+RZT8v1FEpEIFFPjtGCFI3OcW/Vs9uB0x'
AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjEH4aCXVzLXdlc3QtMiJIMEYCIQCjDUQFCrsnqKCk89apj72mHFdA5weq7Ry5Y5dX+XRVnQIhANQVfOO4iz+VXihb5Y05hxeAjaanXYfIJkjhKVgadpAuKsICCNf//////////wEQABoMOTc1MDQ5OTU3OTY2IgwG5gBZyA5A74IIKpQqlgIpLrlaTNfYmNRikjo2tkjWk/Gsxtj7o/z3UAgiIyM3evboCaspEp5jd6BDtHkUqEgg+XsqcqgiqlV6l6+4IAVp7DUvGv6LL1Wt18ZH4gs6MiHcHmh+lGB66+6awRFsmC9LeL1pF1hbvormvrG8+VbGc/hbMEPPWCHeJytjiEmgLrLX8lg5dUYzoN79eG6dC3OBL6d5GByPjuFhW+2wLn3xTkRZJlaVOBWPY5rZoHvPlRzo5RCn359t8Y+jy33n9zI+TCiwdWltRb/RKRGE7bk7bvhPdnmvXK6ZTtpoZorO8Zf9zt2A70NEgYkrcIaI9ZNSoHo97ig4fOD1fOIBjyxhZuh54D/mLxtARTaLR2wdRIF/NpnuLDD/3OixBjqcATd65gUV1D0D+jw2BMlY3HbuSB2IKX/f8lVRM56Xmi5pra5ptGTD+H4J7vBJVyi96lMbJ3ZWPAIwfFqIDqtuqO0xvrKW5EuCzfQk5XFwu8rPoAmdlx5SzT2JoqLTMEuUsJ5oQGl9AvBA1ZPRs4YXwKPacWlpfYDPdbH1mA7hKFfnfT1qyWh9qbA+nlHlXt05/Deq8DkVu3WEUFYdbQ=='
AWS_STORAGE_BUCKET_NAME = 'bravo13-bucket'

# Configura el almacenamiento predeterminado para utilizar S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AVATAR_URL = 's3://bravo13-bucket/avatar/'
COVER_URL = 's3://bravo13-bucket/cover/'
