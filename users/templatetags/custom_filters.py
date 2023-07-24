from django import template

register = template.Library()

@register.filter
def format_float(value, decimal_places=2):
    return f"{value:.{decimal_places}f}"
