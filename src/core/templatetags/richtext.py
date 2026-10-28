from django import template
from django.utils.safestring import mark_safe

from src.core.html_sanitize import sanitize_rich_html

register = template.Library()


@register.filter(name="richhtml")
def richhtml(value):
    text = value if isinstance(value, str) else ""
    return mark_safe(sanitize_rich_html(text))
