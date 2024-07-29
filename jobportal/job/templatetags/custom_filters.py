from django import template

register = template.Library()

@register.filter
def get_count(value):
    # Ensure value is a QuerySet or similar iterable
    if hasattr(value, 'count'):
        return value.count()
    return 0
