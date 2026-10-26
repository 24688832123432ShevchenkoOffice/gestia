from decimal import Decimal

from django.db.models import Prefetch

from src.catalog.models import Product, ProductImage
from src.core.utils import format_money

SESSION_KEY = "cart"
MAX_QTY = 99


def _raw(request):
    data = request.session.get(SESSION_KEY)
    if not isinstance(data, dict):
        data = {}
    return data


def _save(request, data):
    request.session[SESSION_KEY] = data
    request.session.modified = True


def item_count(request) -> int:
    return sum(int(qty) for qty in _raw(request).values())


def set_qty(request, sku: str, qty: int):
    data = _raw(request)
    if qty <= 0:
        data.pop(sku, None)
    else:
        data[sku] = min(int(qty), MAX_QTY)
    _save(request, data)


def add(request, sku: str, qty: int = 1):
    data = _raw(request)
    current = int(data.get(sku, 0))
    data[sku] = min(current + max(int(qty), 1), MAX_QTY)
    _save(request, data)


def clear(request):
    _save(request, {})


def lines(request, currency: str):
    data = _raw(request)
    if not data:
        return [], Decimal("0")
    products = (
        Product.objects.filter(sku__in=list(data.keys()), is_active=True)
        .prefetch_related(Prefetch("images", queryset=ProductImage.objects.order_by("sort", "id")))
    )
    by_sku = {product.sku: product for product in products}
    rows = []
    total = Decimal("0")
    for sku, qty in data.items():
        product = by_sku.get(sku)
        if product is None:
            continue
        qty = int(qty)
        unit = product.amount(currency)
        line_total = unit * qty
        total += line_total
        rows.append(
            {
                "product": product,
                "sku": sku,
                "qty": qty,
                "unit": unit,
                "unit_label": format_money(unit, currency),
                "line_label": format_money(line_total, currency),
                "line_total": line_total,
            }
        )
    return rows, total
