from django import template

register = template.Library()

@register.filter
def times(number):
    try:
        return range(int(number) if number is not None else 0)
    except (ValueError, TypeError):
        return range(0)