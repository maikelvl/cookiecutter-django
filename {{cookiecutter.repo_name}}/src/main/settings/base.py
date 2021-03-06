"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 1.9b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import sys

import environ
from django.utils.translation import ugettext_lazy as _


ROOT_DIR = environ.Path(__file__) - 4  # (/a/b/c/myfile.py - 4 = /)
APPS_DIR = ROOT_DIR.path('src')

env = environ.Env()
try:
    env.read_env(ROOT_DIR.file('.env'))
except (OSError, IOError):
    pass

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('{{ cookiecutter.author_name }}', '{{ cookiecutter.author_email }}'),
)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = (
    {% if cookiecutter.use_django_suit == 'y' %}'suit',{% endif %}
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'sorl.thumbnail',
)

PROJECT_APPS = (
    'main',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates'))
        ],
        'OPTIONS': {
            'context_processors': [
                # Default
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Added
                'django.template.context_processors.i18n',
                # Custom
                'main.context_processors.caches_ttl',
                'main.context_processors.base_url',
                'main.context_processors.debug',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('DJANGO_DATABASE_HOST'),
        'NAME': env('DJANGO_DATABASE_NAME'),
        'USER': env('DJANGO_DATABASE_USER'),
        'PASSWORD': env('DJANGO_DATABASE_PASS'),
        'PORT': env('DJANGO_DATABASE_PORT', default=5432),
        'CONN_MAX_AGE': 300,
    }
}

CACHES_SHORT_TTL = 5 * 60
CACHES_MEDIUM_TTL = 15 * 60
CACHES_LONG_TTL = 60 * 60
CACHES_FOREVER_TTL = 7 * 24 * 60 * 60

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = CACHES_SHORT_TTL
CACHE_MIDDLEWARE_KEY_PREFIX = 'pages'

CACHE_HOST = env('DJANGO_CACHE_HOST')
CACHE_PORT = env('DJANGO_CACHE_PORT', default=6379)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:{}/0'.format(CACHE_HOST, CACHE_PORT),
        'KEY_PREFIX': '{{ cookiecutter.short_name }}',
        'TIMEOUT': CACHES_SHORT_TTL,
        'OPTIONS': {
            'IGNORE_EXCEPTIONS': False,
            'MAX_ENTRIES': 2000,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:{}/1'.format(CACHE_HOST, CACHE_PORT),
        'KEY_PREFIX': '{{ cookiecutter.short_name }}_session',
        'TIMEOUT': 24 * 60 * 60,  # 24 hours, you should use write-through
                                  # cache for session!
        'OPTIONS': {
            'IGNORE_EXCEPTIONS': False,
            'MAX_ENTRIES': sys.maxsize,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'thumbnails': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:{}/2'.format(CACHE_HOST, CACHE_PORT),
        'KEY_PREFIX': '{{ cookiecutter.short_name }}_thumbnails',
        'TIMEOUT': None,
        'OPTIONS': {
            'IGNORE_EXCEPTIONS': False,
            'MAX_ENTRIES': sys.maxsize,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'session'

# AUTH_USER_MODEL = 'users.User'
# LOGIN_URL = 'users:login'
# LOGIN_REDIRECT_URL = 'home'

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='{{ cookiecutter.lang_code }}')
TIME_ZONE = env('DJANGO_TIME_ZONE', default='{{ cookiecutter.timezone }}')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
STATIC_URL = STATIC_HOST + '/static/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = str(ROOT_DIR('media'))

# E-Mail
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='{{ cookiecutter.project_name }} <noreply@{{ '.'.join(cookiecutter.host_name.split('.')[-2:]) }}>')


# Sorl settings
THUMBNAIL_QUALITY = 90
THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_BACKEND = 'main.backends.SEOThumbnailBackend'
THUMBNAIL_PREFIX = 'thumbnails/'
THUMBNAIL_CACHE = 'thumbnails'
THUMBNAIL_REDIS_HOST = CACHE_HOST
THUMBNAIL_REDIS_PORT = CACHE_PORT
THUMBNAIL_REDIS_DB = 2
THUMBNAIL_KEY_PREFIX = CACHES['thumbnails']['KEY_PREFIX']
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

{% if cookiecutter.use_django_suit == 'y' %}SUIT_CONFIG = {
    'ADMIN_NAME': '{{ cookiecutter.project_name }}',
    'HEADER_DATE_FORMAT': 'l j F Y',
    'SEARCH_URL': '',
    # 'MENU': (
    #
    # )
}{% endif %}

# Haystack
DJANGO_ELASTICSEARCH_HOST = env('DJANGO_ELASTICSEARCH_HOST')
DJANGO_ELASTICSEARCH_PORT = env('DJANGO_ELASTICSEARCH_PORT', default=9200)
DJANGO_ELASTICSEARCH_URL = env('DJANGO_ELASTICSEARCH_URL', default='http://{}:{}'.format(DJANGO_ELASTICSEARCH_HOST, DJANGO_ELASTICSEARCH_PORT))

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': DJANGO_ELASTICSEARCH_URL,
        'INDEX_NAME':  env('DJANGO_HAYSTACK_INDEX_NAME', default='{{ cookiecutter.short_name }}'),
        'INCLUDE_SPELLING': True
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

if env('DJANGO_SMTP_HOST', default=False):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('DJANGO_SMTP_HOST')
    EMAIL_PORT = env('DJANGO_SMTP_PORT')
    EMAIL_HOST_USER = env('DJANGO_SMTP_USER')
    EMAIL_HOST_PASSWORD = env('DJANGO_SMTP_PASS')
    EMAIL_USE_TLS = env.bool('DJANGO_SMTP_TLS', default=False)
