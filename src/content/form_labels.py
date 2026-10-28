from src.core.utils import localized

_FIELDS = ("name", "phone", "message", "address", "email")


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
