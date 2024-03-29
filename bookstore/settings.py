"""
Django settings for bookstore project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9owq2o1dckc!9fmnszxvkom!e*w+xb==kwkb&50#=p8j348r8#'           # !!!!!!!!!!!!!!!!!!!!!!!!!!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'registration',                     # django-registration-redux
    'tastypie',
    'bootstrap4',
    'bootstrap_themes',
    'debug_toolbar',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'bookstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'


# Registration (django-registration-redux)
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/store/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = ''                                                    # !!!!!!!!!!!!!!!!!!!!!!!!!!
EMAIL_HOST_PASSWORD = ''                                                # !!!!!!!!!!!!!!!!!!!!!!!!!!
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'books@mysterybooks.com'


# Social Authentication Backends
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',
    'social_core.backends.facebook.FacebookOAuth2',     # for facebook
    'django.contrib.auth.backends.ModelBackend',        # Don’t miss it if using django.contrib.auth application
)

# Additional settings for Facebook
SOCIAL_AUTH_FACEBOOK_KEY = ''                                           # !!!!!!!!!!!!!!!!!!!!!!!!!!
SOCIAL_AUTH_FACEBOOK_SECRET = ''                                        # !!!!!!!!!!!!!!!!!!!!!!!!!!


# PayPal settings
PAYPAL = {
    'client_id': '',                                                    # !!!!!!!!!!!!!!!!!!!!!!!!!!
    'client_secret': '',                                                # !!!!!!!!!!!!!!!!!!!!!!!!!!
    'return_url': 'http://localhost:8000/store/process/paypal',         # !!!!!!!!!!!!!!!!!!!!!!!!!!
    'cancel_url': 'http://localhost:8000/store',                        # !!!!!!!!!!!!!!!!!!!!!!!!!!
}


# For Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(module)s | %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'basic',
            'maxBytes': 10485760,
            'backupCount': 10,
            'filename': os.path.join(BASE_DIR, 'mystery_books.log'),
        },
    },
    'loggers': {
        'store': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }
}
