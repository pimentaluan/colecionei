from django import template
import math

register = template.Library()

@register.filter
def format_number(value):
    if value >= 1000000:
        value = math.floor(value / 100000) / 10
        return '1 milhão' if value == 1 else f'{value:.1f} milhões'
    elif value >= 10000:
        value = math.floor(value / 100) / 10
        return f'{value:.0f} mil' if value.is_integer() else f'{value:.1f} mil'
    elif value >= 1000:
        return f'{value:,}'.replace(',', '.')
    else:
        return value