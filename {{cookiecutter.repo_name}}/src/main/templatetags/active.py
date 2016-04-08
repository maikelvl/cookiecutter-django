import re

from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, path, class_name='active'):
    """
    Return active when request path matches pattern
    """
    request = context.get('request')
    if request and re.search('^{}'.format(re.sub(
            r'^https?://[^/]+', '', path)), request.path):
        return class_name
    return ''


@register.simple_tag(takes_context=True)
def active_reverse(context, name, class_name='active'):
    """
    Return active when request path matches pattern
    """
    request = context.get('request')
    if request and re.search('^{}'.format(re.sub(
            r'^https?://[^/]+', '', reverse(name))), request.path):
        return class_name
    return ''


@register.simple_tag()
def active_compare(value, *values, class_name='active'):
    """
    Return active when value in values list
    """
    if value in values:
        return class_name
    return ''
