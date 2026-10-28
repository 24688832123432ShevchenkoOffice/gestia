import re

from django import forms
from django.utils.translation import gettext_lazy as _

NAME_ALLOWED_RE = re.compile(
    r"^[A-Za-zÀ-ÖØ-öø-ÿА-Яа-яЁёІіЇїЄєҐґ'’ʼ`\- ]+$"
)
NAME_LETTER_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿА-Яа-яЁёІіЇїЄєҐґ]")
PHONE_LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]")

MSG_REQUIRED = _("Поле обов'язкове для заповнення")
MSG_NAME = _(
    "Ім'я не може містити цифри або спецсимволи. Будь ласка, використовуйте лише букви"
)
MSG_NAME_SHORT = _("Занадто коротке значення")
MSG_PHONE = _("Введіть коректний номер мобільного телефону у форматі +380 (XX) XXX-XX-XX")
MSG_EMAIL = _("Некоректний формат")

NAME_ERRORS = {"required": MSG_REQUIRED}
PHONE_ERRORS = {"required": MSG_REQUIRED}
EMAIL_ERRORS = {"required": MSG_REQUIRED, "invalid": MSG_EMAIL}


def clean_name_value(name: str) -> str:
    name = re.sub(r"\s+", " ", (name or "").strip())
    if not name:
        raise forms.ValidationError(MSG_REQUIRED)
    if not NAME_ALLOWED_RE.fullmatch(name):
        raise forms.ValidationError(MSG_NAME)
    if len(NAME_LETTER_RE.findall(name)) < 2:
        raise forms.ValidationError(MSG_NAME_SHORT)
    return name


def clean_phone_value(phone: str) -> str:
    phone = (phone or "").strip()
    if not phone:
        raise forms.ValidationError(MSG_REQUIRED)
    if PHONE_LETTER_RE.search(phone):
        raise forms.ValidationError(MSG_PHONE)
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("380") and len(digits) == 12:
        return f"+{digits}"
    if digits.startswith("0") and len(digits) == 10:
        return f"+38{digits}"
    if len(digits) == 9:
        return f"+380{digits}"
    raise forms.ValidationError(MSG_PHONE)
