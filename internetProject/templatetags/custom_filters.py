from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(value):
    return range(1, value + 1)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, None)