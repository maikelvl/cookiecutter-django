from __future__ import unicode_literals

from decimal import Decimal
from urllib.parse import urlparse

import bleach
from django import template
from django.template.defaultfilters import stringfilter
from django.utils import six
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag(takes_context=True)
def paginator_get_params(context, page_number):
    params = context['request'].GET.copy()
    params[_('pagina')] = page_number
    params.pop('_pjax', None)
    return '?{}'.format(params.urlencode())


@register.simple_tag(takes_context=True)
def filter_build_params(context, key=None, value=''):
    params = context['request'].GET.copy()
    for k in list(params):
        if k in ['o', 'ot']:
            continue
        params.pop(k, None)
    if key:
        params[key] = value
    if len(params):
        return '?{}'.format(params.urlencode())
    return ''


@register.simple_tag(takes_context=True)
def filter_active(context, key=None, value='', class_name='active'):
    params = context['request'].GET
    return class_name if params.get(key, None) == str(value) else ''


@register.simple_tag(takes_context=True)
def form_action_params(context, form, *args):
    # remove form fields from get parameters
    params = context['request'].GET.copy()
    params.pop('_pjax', None)

    for name, field in form.fields.items():
        params.pop(form[name].html_name, None)
    for arg in args:
        params.pop(arg, None)
    return '?{}'.format(params.urlencode())


@register.filter
@stringfilter
def replace(value, arg):
    if not isinstance(value, six.string_types) or value == 'None':
        return ''

    if not isinstance(arg, six.string_types):
        return value

    try:
        search, replacer = arg.split(',', 1)
    except ValueError:
        return value

    return value.replace(search, replacer)


@register.filter
def bleach_tags(value):
    return bleach.clean(value, tags=[], attributes=[], styles=[], strip=True,
                        strip_comments=True)


@register.filter
@stringfilter
def clean_url(value):
    if not isinstance(value, six.string_types) or value == 'None':
        return ''
    scheme, netloc, path, params, query, fragment = urlparse(value)
    return '{}{}'.format(netloc, path.split('/', 1)[0])


@register.filter
def trunc_number_with_dot(value, decimals=2):
    if value is None:
        return ""

    if isinstance(value, six.string_types):
        if value == "":
            return ""

        value = value.replace(',', '.')
        try:
            value = float(value)
        except (TypeError, ValueError):
            return ""

    if isinstance(value, int):
        value = float(value)

    if isinstance(value, Decimal) or isinstance(value, float):
        # Decimals are truncated, not rounded.
        # Note that default float format ({.2f}) rounds before truncate.

        if isinstance(value, Decimal):
            value = '{value:.{count}f}'.format(value=value, count=decimals + 2)
        else:
            value = str(value)

        numb, dec = value.split('.')
        dec = dec[:decimals]
        return '{numb}.{dec:0<{decimal_count}}'.format(
            numb=numb, dec=dec, decimal_count=decimals)

    return str(value)
