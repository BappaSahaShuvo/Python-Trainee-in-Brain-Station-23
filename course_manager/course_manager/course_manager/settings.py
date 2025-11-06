# course_manager/settings.py
import os
from pathlib import Path

# BASE_DIR: project root path (course_manager/)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: keep secret in production. This is a placeholder for local dev.
SECRET_KEY = 'django-insecure-REPLACE_THIS_WITH_A_STRONG_KEY'

# DEBUG: set True for development (shows detailed error pages)
DEBUG = True

# ALLOWED_HOSTS: hosts/domains that can serve the site. Empty for local dev.
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',        # admin site
    'django.contrib.auth',         # authentication system
    'django.contrib.contenttypes', # content types framework
    'django.contrib.sessions',     # session framework
    'django.contrib.messages',     # messaging framework
    'django.contrib.staticfiles',  # static files handling
    'courses',                     # our app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # session handling
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',             # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'course_manager.urls'  # root URL configuration module

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Tell Django where templates live. We include BASE_DIR / "templates" if any.
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # enable looking into app/templates/
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

WSGI_APPLICATION = 'course_manager.wsgi.application'  # WSGI callable

# Database - use SQLite for simplicity
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation (default validators)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JS, images)
STATIC_URL = '/static/'                         # URL prefix for static files
STATICFILES_DIRS = [BASE_DIR / 'static']        # additional dirs for static files
STATIC_ROOT = BASE_DIR / 'staticfiles'          # collectstatic target (for production)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
