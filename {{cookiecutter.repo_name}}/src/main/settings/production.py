{% if cookiecutter.use_aws_s3 == 'y' %}from boto.s3.connection import OrdinaryCallingFormat{% endif %}
from django.utils import six

from .base import *


DEBUG = TEMPLATE_DEBUG = False

SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True

{% if cookiecutter.opbeat_production_app_id != '' %}# See https://opbeat.com/languages/django/
INSTALLED_APPS += ('opbeat.contrib.django',)

OPBEAT = {
    'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
    'APP_ID': env('DJANGO_OPBEAT_APP_ID'),
    'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN')
}

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
) + MIDDLEWARE_CLASSES{% endif %}

{% if cookiecutter.use_aws_s3 == 'y' %}# AWS S3 media setup
AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_HOST = env('DJANGO_AWS_S3_HOST', default='s3-eu-west-1.amazonaws.com')
AWS_S3_CUSTOM_DOMAIN = env('DJANGO_AWS_S3_CUSTOM_DOMAIN', default=None)
AWS_LOCATION = env('DJANGO_AWS_S3_LOCATION', default='media')
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_URL = '//{}/{}/media/'.format(
    AWS_S3_CUSTOM_DOMAIN or AWS_S3_HOST, AWS_STORAGE_BUCKET_NAME){% endif %}
