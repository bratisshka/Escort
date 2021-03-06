from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

STATICFILES_DIRS = (PROJ_DIR / 'static',)

MEDIA_ROOT = str(PROJ_DIR / 'media')

ALLOWED_HOSTS.extend(['testserver', '127.0.0.1', 'localhost'])