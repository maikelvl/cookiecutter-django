from django.contrib import sitemaps
from django.core.urlresolvers import reverse


class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)
