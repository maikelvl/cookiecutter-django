from django.conf import settings
from django.test.testcases import TestCase
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.default import backend

from main.backends import SEOThumbnailBackend
from main.tests.helpers import get_image


class SEOThumbnailBackendTestCase(TestCase):

    def test_settings(self):
        assert getattr(settings, 'THUMBNAIL_BACKEND', '').endswith(
            'SEOThumbnailBackend')

    def test_sorl_backend(self):
        assert isinstance(backend, SEOThumbnailBackend)

    def test_filename(self):
        im = get_thumbnail(get_image('seothumb_test.png'),
                           '100x100', crop='center', quality=99)

        assert 'seothumb_test' in im.name
        assert '.png' in im.name

    def test_identical(self):
        im1 = get_thumbnail(get_image('foobar.png'), '100x100')
        im2 = get_thumbnail(get_image('foobar.png'), '100x100')

        assert im1.name == im2.name

    def test_unique_name(self):
        im1 = get_thumbnail(get_image('foobar.png'), '256x256')
        im2 = get_thumbnail(get_image('lorem.png'), '256x256')

        assert im1.name != im2.name

    def test_unique_crop(self):
        im1 = get_thumbnail(get_image('foobar.png'), '100x100')
        im2 = get_thumbnail(get_image('foobar.png'), '100x100', crop='center')

        assert im1.name != im2.name

    def test_unique_size(self):
        im1 = get_thumbnail(get_image('foobar.png'), '50x200')
        im2 = get_thumbnail(get_image('foobar.png'), '100x100')

        assert im1.name != im2.name

    def test_unique_size2(self):
        im1 = get_thumbnail(get_image('foobar.png'), 'x99')
        im2 = get_thumbnail(get_image('foobar.png'), '1000x1000')

        assert im1.name != im2.name
