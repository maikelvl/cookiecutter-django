from math import ceil as math_ceil

from django import template


register = template.Library()


@register.filter("mult", is_safe=False)
def mult(value, arg):
    """Multiplies the arg and the value"""
    return float(value) * int(arg)


@register.filter("sub", is_safe=False)
def sub(value, arg):
    """Subtracts the arg from the value"""
    return float(value) - int(arg)


@register.filter("div", is_safe=False)
def div(value, arg):
    """Divides the value by the arg"""
    return float(value) / int(arg)


@register.filter("ceil", is_safe=False)
def ceil(value):
    """Ceils value"""
    return math_ceil(float(value))


@register.filter("addf", is_safe=False)
def addf(value, arg):
    """Adds the arg to the value."""
    return float(value) + float(arg)
