from django.db.utils import OperationalError, ProgrammingError

from src.core.utils import localized

_FIELDS = ("name", "phone", "message", "address", "email")


def label_form(form):
    from src.content.models import ContactForms

    try:
        copy = ContactForms.load()
    except (OperationalError, ProgrammingError):
        return form
    return apply_labels(form, copy)


def apply_labels(form, copy):
    if form is None or copy is None:
        return form
    for name in _FIELDS:
        if name not in form.fields or not hasattr(copy, f"label_{name}_uk"):
            continue
        label = localized(copy, f"label_{name}")
        if label:
            form.fields[name].label = label
    return form
