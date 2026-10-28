"""Санітизація полів, які модель позначила як rich_text_fields."""

from django.db.models.signals import pre_save

from src.core.html_sanitize import sanitize_rich_html


def apply_rich_text_sanitize(instance) -> None:
    names = getattr(instance, "rich_text_fields", None) or ()
    for name in names:
        value = getattr(instance, name, None)
        if isinstance(value, str) and value:
            setattr(instance, name, sanitize_rich_html(value))


def sanitize_rich_text_on_save(sender, instance, **kwargs):
    apply_rich_text_sanitize(instance)


def connect() -> None:
    pre_save.connect(sanitize_rich_text_on_save, dispatch_uid="gestia.richtext.sanitize")
