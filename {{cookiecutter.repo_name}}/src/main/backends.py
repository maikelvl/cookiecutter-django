from os.path import basename

from django.conf import settings
from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.helpers import serialize, tokey


class SEOThumbnailBackend(ThumbnailBackend):
    """
    SEO friendly thumbnail file names
    """
    def _get_thumbnail_filename(self, source, geometry_string, options):
        key = tokey(source.key, geometry_string, serialize(options))
        path = '%s/%s/%s' % (key[:2], key[2:4], key)
        return '%s%s/%s' % (
            settings.THUMBNAIL_PREFIX, path, basename(source.name))
