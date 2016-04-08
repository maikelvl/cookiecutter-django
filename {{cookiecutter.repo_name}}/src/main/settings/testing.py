from model_mommy.generators import gen_image_field

from .base import *


DEBUG = TEMPLATE_DEBUG = False

MOMMY_CUSTOM_FIELDS_GEN = {
    'sorl.thumbnail.fields.ImageField': gen_image_field,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

HAYSTACK_CONNECTIONS['default']['INDEX_NAME'] = '{}_test'.format(
    HAYSTACK_CONNECTIONS['default']['INDEX_NAME'])

# Dummy cache
for key in CACHES:
    CACHES[key]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
