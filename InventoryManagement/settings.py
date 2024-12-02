from pathlib import Path
import sys
from .languages import LANGUAGES  # Adjust the path to where your languages.py is located




# Add the project directory to the path to import config.py
sys.path.append('.')  # This will allow you to import the config.py file from the current directory
from config import DATABASE, SECRET_KEY, DEBUG, ALLOWED_HOSTS  # Import from config.py

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

# ALLOWED_HOSTS
ALLOWED_HOSTS = ALLOWED_HOSTS



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # Ensure GIS is added to installed apps for PostGIS support
    'property',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # This middleware should be included
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


USE_I18N = True  # This enables Django's internationalization system

LANGUAGE_CODE = 'en'  # Default language code for your site, can be overridden by users


ROOT_URLCONF = 'InventoryManagement.urls'

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

WSGI_APPLICATION = 'InventoryManagement.wsgi.application'

# Database configuration from config.py
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Use PostGIS backend
        'NAME': DATABASE['NAME'],
        'USER': DATABASE['USER'],
        'PASSWORD': DATABASE['PASSWORD'],
        'HOST': DATABASE['HOST'],
        'PORT': DATABASE['PORT'],
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GDAL_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgdal.so'
