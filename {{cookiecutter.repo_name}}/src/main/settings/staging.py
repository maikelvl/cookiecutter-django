from .base import *


DEBUG = TEMPLATE_DEBUG = False

HAYSTACK_CONNECTIONS['default']['ENGINE'] = \
    'haystack.backends.simple_backend.SimpleEngine'

{% if cookiecutter.opbeat_staging_app_id != '' %}# See https://opbeat.com/languages/django/
INSTALLED_APPS += ('opbeat.contrib.django',)

OPBEAT = {
    'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
    'APP_ID': env('DJANGO_OPBEAT_APP_ID'),
    'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN')
}

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
) + MIDDLEWARE_CLASSES{% endif %}

CACHES_SHORT_TTL = 0
CACHES_MEDIUM_TTL = 0
CACHES_LONG_TTL = 0
CACHES_FOREVER_TTL = 0
CACHE_MIDDLEWARE_SECONDS = 0
