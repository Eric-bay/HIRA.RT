# tracker/templatetags/filters.py

from django import template

register = template.Library()

@register.filter
def length_is(value, length):
    return len(value) == int(length)