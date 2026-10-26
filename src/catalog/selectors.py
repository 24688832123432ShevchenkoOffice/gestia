from urllib.parse import urlencode

from django.db.models import Q

from src.catalog.models import CatalogCell, Category, Product, ProductAttribute, ProductAttributeGroup

ATTRIBUTE_FILTER_KEYS = (
    ProductAttributeGroup.Slug.STYLE,
    ProductAttributeGroup.Slug.COLOR,
)


def base_products():
    return (
        Product.objects.filter(is_active=True)
        .select_related("category", "category__parent", "product_set")
        .prefetch_related("images", "filter_attrs__group")
    )


def nav_categories():
    roots = (
        Category.objects.filter(parent__isnull=True, is_active=True)
        .prefetch_related("children")
        .order_by("sort", "name_uk")
    )
    return [cat for cat in roots if cat.has_public_products]


def parse_catalog_filters(get):
    attrs = {}
    for key in ATTRIBUTE_FILTER_KEYS:
        values = [value for value in get.getlist(key) if value][:12]
        if values:
            attrs[key] = values
    selected = [f"{key}:{value}" for key, values in attrs.items() for value in values]
    return {
        "attrs": attrs,
        "selected": selected,
        "q": (get.get("q") or "").strip()[:80],
        "in_stock": get.get("in_stock") == "1",
    }


def filter_catalog(qs, parsed):
    query = parsed["q"]
    if query:
        qs = qs.filter(
            Q(name_uk__icontains=query)
            | Q(name_ru__icontains=query)
            | Q(name_en__icontains=query)
            | Q(sku__iexact=query)
        )
    for key, values in parsed["attrs"].items():
        qs = qs.filter(filter_attrs__group__slug=key, filter_attrs__slug__in=values)
    if parsed["in_stock"]:
        qs = qs.filter(stock_status=Product.Stock.IN_STOCK)
    return qs.distinct()


def category_scope(category):
    ids = [category.pk]
    ids.extend(category.children.filter(is_active=True).values_list("pk", flat=True))
    return ids


def filter_groups_for_catalog(product_qs):
    ids = product_qs.values_list("pk", flat=True)
    groups = []
    for group in ProductAttributeGroup.objects.filter(slug__in=ATTRIBUTE_FILTER_KEYS):
        values = (
            ProductAttribute.objects.filter(
                group=group,
                is_filterable=True,
                products__pk__in=ids,
                products__is_active=True,
            )
            .distinct()
            .order_by("name_uk")
        )
        if values:
            groups.append({"group": group, "values": list(values)})
    return groups


def catalog_bands():
    cells = (
        CatalogCell.objects.select_related("product", "product__category")
        .prefetch_related("product__images")
        .order_by("band", "sort", "id")
    )
    bands = []
    index = {}
    for cell in cells:
        band = index.get(cell.band)
        if band is None:
            band = {"layout": cell.layout, "grid": [], "feature": []}
            index[cell.band] = band
            bands.append(band)
        key = "feature" if cell.role == CatalogCell.Role.FEATURE else "grid"
        band[key].append(cell)
    return bands


def filters_reset_url(request):
    query = (request.GET.get("q") or "").strip()
    if query:
        return f"{request.path}?{urlencode({'q': query})}"
    return request.path


def same_set(product, limit=4):
    if not product.product_set_id:
        return Product.objects.none()
    return (
        base_products()
        .filter(product_set=product.product_set)
        .exclude(pk=product.pk)[:limit]
    )


def related_products(product, limit=4):
    set_ids = []
    if product.product_set_id:
        set_ids = list(
            product.product_set.products.exclude(pk=product.pk).values_list("pk", flat=True)
        )
    manual = list(
        base_products()
        .filter(pk__in=product.related_manual.filter(is_active=True).values("pk"))
        .exclude(pk__in=set_ids)[:limit]
    )
    if len(manual) >= limit:
        return manual
    attr_ids = list(product.filter_attrs.values_list("pk", flat=True))
    taken = [item.pk for item in manual] + set_ids
    auto = (
        base_products()
        .filter(Q(category=product.category) | Q(filter_attrs__in=attr_ids))
        .exclude(pk=product.pk)
        .exclude(pk__in=taken)
        .distinct()[: limit - len(manual)]
    )
    return manual + list(auto)
