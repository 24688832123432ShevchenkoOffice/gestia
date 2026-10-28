from django import template
from django.utils.translation import get_language

from src.content.literals import LITERALS
from src.core.utils import localized

register = template.Library()


def _literal(key):
    uk, en = LITERALS[key]
    lang = (get_language() or "uk").split("-")[0]
    if lang == "en" and en:
        return en
    return uk


def _filled(value):
    return isinstance(value, str) and bool(value.strip())


@register.simple_tag
def cms(value, key):
    if _filled(value):
        return value
    return _literal(key)


@register.simple_tag
def cms_field(obj, field):
    value = ""
    if obj is not None and hasattr(obj, f"{field}_uk"):
        value = localized(obj, field)
    if _filled(value):
        return value
    return _literal(field)
