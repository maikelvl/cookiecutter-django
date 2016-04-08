from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from main.views import OpenSearchXMLView

from .views import ErrorView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^beheer/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(
        template_name='humans.txt', content_type='text/plain'),
        name='humans.txt'),

    # url(r'^zoeken/$', SearchView.as_view(), name='search'),
    # url(r'^opensearch\.xml$', OpenSearchXMLView.as_view(), name="opensearch"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        url(r'^400/', ErrorView.as_view(
            status_code=200, template_name='400.html')),
        url(r'^403/', ErrorView.as_view(
            status_code=200, template_name='403.html')),
        url(r'^404/', ErrorView.as_view(
            status_code=200, template_name='404.html')),
        url(r'^500/', ErrorView.as_view(
            status_code=200, template_name='500.html')),
    ]

handler400 = ErrorView.rendered_view(status_code=400, template_name='400.html')
handler403 = ErrorView.rendered_view(status_code=403, template_name='403.html')
handler404 = ErrorView.rendered_view(status_code=404, template_name='404.html')
handler500 = ErrorView.rendered_view(status_code=500, template_name='500.html')
