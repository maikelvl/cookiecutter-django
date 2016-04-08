from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def caches_ttl(request):
    """ Cache TTL's """
    return {
        'SHORT_TTL': settings.CACHES_SHORT_TTL,
        'MEDIUM_TTL': settings.CACHES_MEDIUM_TTL,
        'LONG_TTL': settings.CACHES_LONG_TTL,
        'FOREVER_TTL': settings.CACHES_FOREVER_TTL,
    }


def base_url(request):
    context = dict()
    context['domain'] = get_current_site(request).domain
    context['domain_no_port'] = context['domain'].split(':')[0]
    context['protocol'] = 'https' if request.is_secure() else 'http'
    context['base_url'] = '{}://{}'.format(
        context['protocol'], context['domain'])

    return context


def debug(request):
    return {
        'debug': settings.DEBUG
    }
