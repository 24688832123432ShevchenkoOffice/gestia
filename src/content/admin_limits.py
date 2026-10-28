from django.core.validators import MaxLengthValidator


def tighten(formfield, limit=None, hint=""):
    if formfield is None:
        return None
    if limit:
        formfield.max_length = limit
        formfield.widget.attrs["maxlength"] = str(limit)
        formfield.validators = [
            item for item in formfield.validators if not isinstance(item, MaxLengthValidator)
        ]
        formfield.validators.append(MaxLengthValidator(limit))
    if hint:
        formfield.help_text = hint
    return formfield
