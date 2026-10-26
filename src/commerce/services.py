import secrets
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language

from src.catalog.models import Product
from src.commerce.models import Inquiry, Order, OrderItem
from src.commerce.notify import notify_inquiry, notify_order


def _number() -> str:
    stamp = timezone.now().strftime("%y%m%d")
    return f"GS{stamp}-{secrets.token_hex(2).upper()}"


def _pay_status(method: str) -> str:
    if method == Order.Payment.CARD:
        return Order.PayStatus.AWAITING
    return Order.PayStatus.UNPAID


@transaction.atomic
def create_order(*, source, customer, rows, currency, language):
    total = sum((row["line_total"] for row in rows), Decimal("0"))
    order = Order.objects.create(
        number=_number(),
        source=source,
        customer_name=customer["name"],
        phone=customer["phone"],
        email=customer.get("email", ""),
        language=language or get_language() or "uk",
        currency=currency,
        delivery_method=customer["delivery_method"],
        delivery_address=customer["address"],
        payment_method=customer["payment_method"],
        payment_status=_pay_status(customer["payment_method"]),
        total=total,
        consent=True,
    )
    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                sku=row["sku"],
                name=row["name"],
                qty=row["qty"],
                unit_price=row["unit"],
            )
            for row in rows
        ]
    )
    order_id = order.pk
    transaction.on_commit(lambda oid=order_id: notify_order(oid))
    return order


def row_from_product(product: Product, qty: int, currency: str):
    unit = product.amount(currency)
    return {
        "sku": product.sku,
        "name": product.name_uk,
        "qty": qty,
        "unit": unit,
        "line_total": unit * qty,
    }


@transaction.atomic
def create_inquiry(*, kind, name, phone, consent, message="", email="", sku=""):
    product = None
    product_name = ""
    if sku:
        product = Product.objects.filter(sku=sku, is_active=True).first()
        if product:
            product_name = product.name_uk
            sku = product.sku
    inquiry = Inquiry.objects.create(
        kind=kind,
        name=name,
        phone=phone,
        email=email,
        message=message,
        product=product,
        product_name=product_name,
        sku=sku,
        consent=consent,
    )
    inquiry_id = inquiry.pk
    transaction.on_commit(lambda iid=inquiry_id: notify_inquiry(iid))
    return inquiry
