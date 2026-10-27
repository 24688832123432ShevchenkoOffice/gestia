from decimal import Decimal

from django import template

from src.core.utils import format_money

register = template.Library()


def _grouped(amount):
    whole = int(Decimal(amount).quantize(Decimal("1")))
    return f"{whole:,}".replace(",", " ")


@register.simple_tag(takes_context=True)
def money(context, amount):
    return format_money(amount, context.get("currency") or "uah")


@register.simple_tag(takes_context=True)
def product_price(context, product):
    currency = context.get("currency") or "uah"
    amount = product.price_eur if currency == "eur" else product.price_uah
    return format_money(amount, currency)


@register.filter
def figma_nbsp(value):
    return str(value).replace(" ", "\u00a0")


@register.simple_tag(takes_context=True)
def line_uah(context, amount):
    currency = context.get("currency") or "uah"
    if currency == "eur":
        return format_money(amount, "eur")
    return f"{_grouped(amount)} UAH"


@register.simple_tag(takes_context=True)
def sum_uah(context, amount):
    currency = context.get("currency") or "uah"
    if currency == "eur":
        return format_money(amount, "eur")
    return f"₴ {_grouped(amount)} грн"


@register.simple_tag(takes_context=True)
def home_price(context, product):
    currency = context.get("currency") or "uah"
    if currency == "eur":
        return format_money(product.price_eur, "eur")
    return f"{_grouped(product.price_uah)} UAH"
