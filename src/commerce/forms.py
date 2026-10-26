import re

from django import forms
from django.utils.translation import gettext_lazy as _

from src.commerce.models import Order

PHONE_RE = re.compile(r"^[0-9+\-() ]{10,20}$")
LETTER_RE = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ]")


def clean_phone_value(phone: str) -> str:
    phone = (phone or "").strip()
    digits = re.sub(r"\D", "", phone)
    if LETTER_RE.search(phone) or not PHONE_RE.match(phone) or len(digits) < 10:
        raise forms.ValidationError(_("Укажіть телефон цифрами, без літер."))
    return phone


class ConsentForm(forms.Form):
    consent = forms.BooleanField(label=_("Погоджуюсь на обробку персональних даних"), required=True)


class ContactForm(ConsentForm):
    name = forms.CharField(label=_("Ім'я"), max_length=120)
    phone = forms.CharField(label=_("Телефон"), max_length=32)
    message = forms.CharField(label=_("Повідомлення"), required=False, widget=forms.Textarea(attrs={"rows": 4}))

    def clean_phone(self):
        return clean_phone_value(self.cleaned_data["phone"])


class CallbackForm(ConsentForm):
    name = forms.CharField(label=_("Ім'я"), max_length=120)
    phone = forms.CharField(label=_("Телефон"), max_length=32)
    sku = forms.CharField(widget=forms.HiddenInput)

    def clean_phone(self):
        return clean_phone_value(self.cleaned_data["phone"])


class BuyNowForm(ConsentForm):
    name = forms.CharField(label=_("Ім'я"), max_length=120)
    phone = forms.CharField(label=_("Телефон"), max_length=32)
    address = forms.CharField(label=_("Адреса доставки"), max_length=255)
    sku = forms.CharField(widget=forms.HiddenInput)

    def clean_phone(self):
        return clean_phone_value(self.cleaned_data["phone"])


class CheckoutForm(ConsentForm):
    name = forms.CharField(label=_("Ім'я"), max_length=120)
    phone = forms.CharField(label=_("Телефон"), max_length=32)
    email = forms.EmailField(label=_("Email"))
    delivery_method = forms.ChoiceField(label=_("Доставка"), choices=Order.Delivery.choices)
    address = forms.CharField(label=_("Адреса доставки"), max_length=255)
    payment_method = forms.ChoiceField(label=_("Оплата"), choices=Order.Payment.choices)

    def clean_phone(self):
        return clean_phone_value(self.cleaned_data["phone"])


def style_form(form):
    for name, field in form.fields.items():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs["class"] = "field__check"
        elif isinstance(field.widget, forms.Textarea):
            field.widget.attrs["class"] = "field__input field__input--area"
        elif not isinstance(field.widget, forms.HiddenInput):
            field.widget.attrs["class"] = "field__input"
        if name == "phone":
            field.widget.attrs.update({"inputmode": "tel", "autocomplete": "tel"})
        if name == "name":
            field.widget.attrs["autocomplete"] = "name"
        if name == "email":
            field.widget.attrs["autocomplete"] = "email"
        if name in {"address"}:
            field.widget.attrs["autocomplete"] = "street-address"
    return form
