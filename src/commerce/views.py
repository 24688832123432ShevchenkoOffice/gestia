from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from src.catalog.models import Product
from src.commerce.cart import add, clear, lines, set_qty
from src.commerce.forms import BuyNowForm, CallbackForm, CheckoutForm, ContactForm, style_form
from src.commerce.models import Inquiry, Order
from src.commerce.services import create_inquiry, create_order, row_from_product
from src.core.utils import format_money


def _currency(request):
    currency = request.session.get("currency", "uah")
    return currency if currency in {"uah", "eur"} else "uah"


def _hx(request):
    return request.headers.get("HX-Request")


def cart_page(request):
    rows, total = lines(request, _currency(request))
    return render(
        request,
        "commerce/cart.html",
        {"rows": rows, "total": total, "total_label": format_money(total, _currency(request))},
    )


def checkout(request):
    currency = _currency(request)
    rows, total = lines(request, currency)
    if not rows:
        return HttpResponseRedirect(reverse("cart"))
    form = style_form(CheckoutForm(request.POST or None))
    if request.method == "POST" and form.is_valid():
        order = create_order(
            source=Order.Source.CART,
            customer={
                "name": form.cleaned_data["name"],
                "phone": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "delivery_method": form.cleaned_data["delivery_method"],
                "address": form.cleaned_data["address"],
                "payment_method": form.cleaned_data["payment_method"],
            },
            rows=[
                {
                    "sku": row["sku"],
                    "name": row["product"].name_uk,
                    "qty": row["qty"],
                    "unit": row["unit"],
                    "line_total": row["line_total"],
                }
                for row in rows
            ],
            currency=currency,
            language=request.LANGUAGE_CODE,
        )
        clear(request)
        return HttpResponseRedirect(f"{reverse('thanks')}?kind=order&number={order.number}")
    return render(
        request,
        "commerce/checkout.html",
        {"form": form, "rows": rows, "total": total, "total_label": format_money(total, currency)},
    )


def thanks(request):
    kind = request.GET.get("kind", "order")
    return render(
        request,
        "commerce/thanks.html",
        {"kind": kind, "number": request.GET.get("number", "")},
    )


@require_POST
def cart_add(request):
    product = get_object_or_404(Product, sku=request.POST.get("sku", ""), is_active=True)
    if product.stock_status == Product.Stock.OUT:
        return HttpResponse(status=422)
    try:
        qty = int(request.POST.get("qty", "1"))
    except (TypeError, ValueError):
        qty = 1
    add(request, product.sku, qty)
    if _hx(request):
        return render(request, "partials/cart_count.html", {"cart_count": sum_count(request)})
    return HttpResponseRedirect(product.get_absolute_url())


def sum_count(request):
    from src.commerce.cart import item_count

    return item_count(request)


@require_POST
def cart_update(request):
    sku = request.POST.get("sku", "")
    try:
        qty = int(request.POST.get("qty", "1"))
    except ValueError:
        qty = 1
    set_qty(request, sku, qty)
    if _hx(request):
        currency = _currency(request)
        rows, total = lines(request, currency)
        response = render(
            request,
            "commerce/_cart_body.html",
            {"rows": rows, "total": total, "total_label": format_money(total, currency)},
        )
        return response
    return HttpResponseRedirect(reverse("cart"))


@require_POST
def callback(request):
    form = style_form(CallbackForm(request.POST))
    if not form.is_valid():
        status = 422 if _hx(request) else 200
        return render(request, "commerce/_callback_form.html", {"callback_form": form}, status=status)
    create_inquiry(
        kind=Inquiry.Kind.CALLBACK,
        name=form.cleaned_data["name"],
        phone=form.cleaned_data["phone"],
        sku=form.cleaned_data["sku"],
        consent=True,
    )
    return render(request, "commerce/_thanks_lead.html", {"long": True})


@require_POST
def buy_now(request):
    form = style_form(BuyNowForm(request.POST))
    product = Product.objects.filter(sku=request.POST.get("sku", ""), is_active=True).first()
    valid = form.is_valid()
    if product is None or product.stock_status == Product.Stock.OUT:
        form.add_error(None, _("Цей товар зараз не можна замовити."))
        valid = False
    if not valid or product is None:
        status = 422 if _hx(request) else 200
        return render(request, "commerce/_buy_form.html", {"buy_form": form}, status=status)
    currency = _currency(request)
    order = create_order(
        source=Order.Source.BUY_NOW,
        customer={
            "name": form.cleaned_data["name"],
            "phone": form.cleaned_data["phone"],
            "email": "",
            "delivery_method": Order.Delivery.COURIER,
            "address": form.cleaned_data["address"],
            "payment_method": Order.Payment.ON_DELIVERY,
        },
        rows=[row_from_product(product, 1, currency)],
        currency=currency,
        language=request.LANGUAGE_CODE,
    )
    if _hx(request):
        response = HttpResponse()
        response["HX-Redirect"] = f"{reverse('thanks')}?kind=order&number={order.number}"
        return response
    return HttpResponseRedirect(f"{reverse('thanks')}?kind=order&number={order.number}")


@require_POST
def contact(request):
    form = style_form(ContactForm(request.POST))
    if not form.is_valid():
        status = 422 if _hx(request) else 200
        return render(request, "commerce/_contact_form.html", {"contact_form": form}, status=status)
    create_inquiry(
        kind=Inquiry.Kind.CONTACT,
        name=form.cleaned_data["name"],
        phone=form.cleaned_data["phone"],
        message=form.cleaned_data["message"],
        consent=True,
    )
    return render(request, "commerce/_thanks_lead.html", {"long": False})
