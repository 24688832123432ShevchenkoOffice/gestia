from django.http import Http404
from django.shortcuts import get_object_or_404, render

from src.catalog.models import Category, Product
from src.catalog.selectors import (
    base_products,
    catalog_bands,
    category_scope,
    filter_catalog,
    filter_groups_for_catalog,
    filters_reset_url,
    parse_catalog_filters,
    related_products,
    same_set,
)
from src.commerce.forms import BuyNowForm, CallbackForm, style_form
from src.content.models import HomeBlock


def _filters_active(parsed):
    return bool(parsed["q"] or parsed["in_stock"] or parsed["attrs"])


def _catalog_context(request, category=None):
    parsed = parse_catalog_filters(request.GET)
    qs = base_products()
    if category:
        qs = qs.filter(category_id__in=category_scope(category))
    facet_base = qs
    products = filter_catalog(qs, parsed)
    active = _filters_active(parsed)
    bands = [] if active else catalog_bands()
    block = HomeBlock.objects.filter(key=HomeBlock.Key.CATALOG).first()
    subcategories = []
    if category:
        subcategories = [child for child in category.children.filter(is_active=True) if child.has_public_products]
    else:
        subcategories = [
            cat
            for cat in Category.objects.filter(parent__isnull=True, is_active=True).order_by("sort")
            if cat.has_public_products
        ]
    return {
        "category": category,
        "products": products,
        "parsed": parsed,
        "filter_groups": filter_groups_for_catalog(facet_base),
        "subcategories": subcategories,
        "filters_reset_url": filters_reset_url(request),
        "crumbs": category.chain() if category else [],
        "catalog_bands": bands,
        "show_mosaic": bool(bands),
        "catalog_cta": block.cta if block else "",
    }


def catalog(request, slug=None):
    category = None
    if slug:
        category = get_object_or_404(Category, slug=slug, is_active=True)
    context = _catalog_context(request, category)
    template = "catalog/_results.html" if request.headers.get("HX-Request") else "catalog/list.html"
    return render(request, template, context)


def product_detail(request, slug):
    product = get_object_or_404(base_products(), slug=slug)
    if not product.is_active:
        raise Http404
    attrs = [attr for attr in product.filter_attrs.all() if attr.show_on_pdp]
    return render(
        request,
        "catalog/product.html",
        {
            "product": product,
            "attrs": attrs,
            "set_products": same_set(product),
            "related": related_products(product),
            "crumbs": product.category.chain(),
            "callback_form": style_form(CallbackForm(initial={"sku": product.sku})),
            "buy_form": style_form(BuyNowForm(initial={"sku": product.sku})),
        },
    )
