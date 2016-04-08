from .base import *


DEBUG = THUMBNAIL_DEBUG = True

USE_REDIS = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'debug_toolbar',
    'debug_panel',
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False if r.is_ajax() else True,
}

MIDDLEWARE_CLASSES += [
    'debug_panel.middleware.DebugPanelMiddleware',
]

# Remove cached loader
TEMPLATES[0]['OPTIONS']['loaders'] = TEMPLATES[0]['OPTIONS']['loaders'][0][1]
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

if not USE_REDIS:
    THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

    # Dummy cache
    for key in CACHES:
        CACHES[key]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

# Add this line if you like to use dynamic dummy images
# THUMBNAIL_DUMMY = True
THUMBNAIL_DUMMY_SOURCE = 'http://placeimg.com/%(width)s/%(height)s/any'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = []

CACHES_SHORT_TTL = 0
CACHES_MEDIUM_TTL = 0
CACHES_LONG_TTL = 0
CACHES_FOREVER_TTL = 0
CACHE_MIDDLEWARE_SECONDS = 0
