"""Дерево сайдбара Unfold.

Новий пункт — dict у NAV_TREE:

    {"key": "stable-id", "title": "Назва", "icon": "home", "url_name": "admin:app_model_changelist"}

Порожній url_name або неіснуючий admin URL у меню не потрапляє.
query додається до changelist (фільтр існуючої моделі).
"""

from django.http import QueryDict
from django.urls import NoReverseMatch, reverse, reverse_lazy


NAV_TREE = [
    {
        "title": "Головна",
        "items": [
            {
                "key": "home_hero",
                "title": "Головний банер",
                "icon": "view_carousel",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=hero",
            },
            {
                "key": "home_categories",
                "title": "Категорії",
                "icon": "grid_view",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=categories",
            },
            {
                "key": "home_video",
                "title": "Відео",
                "icon": "smart_display",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=video",
            },
            {
                "key": "home_popular",
                "title": "Популярні товари",
                "icon": "star",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=popular",
            },
            {
                "key": "home_advantages",
                "title": "Переваги",
                "icon": "verified",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=advantages",
            },
            {
                "key": "home_advantage_cards",
                "title": "Картки переваг",
                "icon": "dashboard",
                "url_name": "admin:content_advantage_changelist",
            },
            {
                "key": "home_video_2",
                "title": "Відео 2",
                "icon": "smart_display",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=video_2",
            },
            {
                "key": "home_reviews",
                "title": "Відгуки",
                "icon": "reviews",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=reviews",
            },
            {
                "key": "home_review_list",
                "title": "Список відгуків",
                "icon": "format_quote",
                "url_name": "admin:content_review_changelist",
            },
            {
                "key": "home_callback",
                "title": "Зворотний дзвінок",
                "icon": "call",
                "url_name": "admin:content_homeblock_changelist",
                "query": "key__exact=callback",
            },
            {
                "key": "home_cta",
                "title": "CTA та контактні форми",
                "icon": "mail",
                "url_name": "",
            },
        ],
    },
    {
        "title": "Про нас",
        "items": [
            {
                "key": "about",
                "title": "Про нас",
                "icon": "info",
                "url_name": "admin:content_aboutpage_changelist",
            },
        ],
    },
    {
        "title": "Каталог",
        "items": [
            {
                "key": "catalog_products",
                "title": "Товари",
                "icon": "inventory_2",
                "url_name": "admin:catalog_product_changelist",
            },
            {
                "key": "catalog_categories",
                "title": "Категорії",
                "icon": "category",
                "url_name": "admin:catalog_category_changelist",
            },
            {
                "key": "catalog_sets",
                "title": "Сети",
                "icon": "layers",
                "url_name": "admin:catalog_productset_changelist",
            },
            {
                "key": "catalog_attributes",
                "title": "Атрибути",
                "icon": "tune",
                "url_name": "admin:catalog_productattribute_changelist",
                "items": [
                    {
                        "key": "catalog_attribute_groups",
                        "title": "Групи атрибутів",
                        "icon": "account_tree",
                        "url_name": "admin:catalog_productattributegroup_changelist",
                    },
                ],
            },
            {
                "key": "catalog_frames",
                "title": "Фрейми каталогу",
                "icon": "grid_on",
                "url_name": "admin:catalog_catalogcell_changelist",
            },
        ],
    },
    {
        "title": "Знижка",
        "items": [
            {
                "key": "discount",
                "title": "Знижка",
                "icon": "percent",
                "url_name": "",
            },
        ],
    },
    {
        "title": "Юридичні сторінки",
        "items": [
            {
                "key": "legal_offer",
                "title": "Публічний договір",
                "icon": "gavel",
                "url_name": "",
            },
            {
                "key": "legal_privacy",
                "title": "Політика конфіденційності",
                "icon": "policy",
                "url_name": "admin:content_privacypage_changelist",
            },
            {
                "key": "legal_cookies",
                "title": "Політика cookies",
                "icon": "cookie",
                "url_name": "",
            },
            {
                "key": "legal_shipping",
                "title": "Доставка та оплата",
                "icon": "local_shipping",
                "url_name": "",
            },
        ],
    },
    {
        "title": "Хедер і футер",
        "items": [
            {
                "key": "chrome_header",
                "title": "Шапка і контакти",
                "icon": "web_asset",
                "url_name": "admin:content_sitesettings_changelist",
            },
            {
                "key": "chrome_footer_links",
                "title": "Посилання футера",
                "icon": "link",
                "url_name": "admin:content_footerlink_changelist",
            },
        ],
    },
    {
        "title": "Стилі",
        "items": [
            {
                "key": "styles",
                "title": "Стилі сайту",
                "icon": "palette",
                "url_name": "",
            },
        ],
    },
    {
        "title": "Замовлення і заявки",
        "items": [
            {
                "key": "orders",
                "title": "Замовлення",
                "icon": "receipt_long",
                "url_name": "admin:commerce_order_changelist",
            },
            {
                "key": "inquiries",
                "title": "Заявки",
                "icon": "inbox",
                "url_name": "admin:commerce_inquiry_changelist",
            },
        ],
    },
    {
        "title": "Користувачі",
        "items": [
            {
                "key": "users",
                "title": "Користувачі",
                "icon": "person",
                "url_name": "admin:auth_user_changelist",
            },
            {
                "key": "groups",
                "title": "Групи",
                "icon": "group",
                "url_name": "admin:auth_group_changelist",
            },
        ],
    },
]


def iter_nav_entries(tree=None):
    for group in tree if tree is not None else NAV_TREE:
        yield from _walk(group.get("items") or [])


def build_navigation(request=None):
    groups = []
    for spec in NAV_TREE:
        items = []
        for entry in spec.get("items") or []:
            visible = _visible_item(entry)
            if visible:
                items.append(visible)
        if not items:
            continue
        groups.append(
            {
                "title": spec["title"],
                "separator": bool(groups),
                "collapsible": True,
                "items": items,
            }
        )
    return groups


def _walk(entries):
    for entry in entries:
        yield entry
        yield from _walk(entry.get("items") or [])


def _safe_reverse(url_name):
    if not url_name:
        return None
    try:
        reverse(url_name)
    except NoReverseMatch:
        return None
    return reverse_lazy(url_name)


def _link(url_name, query):
    lazy_link = _safe_reverse(url_name)
    if lazy_link is None:
        return None
    if not query:
        return lazy_link

    def href(request=None, name=url_name, extra=query):
        return f"{reverse(name)}?{extra}"

    return href


def _active(url_name, query):
    def active(request):
        try:
            path = reverse(url_name)
        except NoReverseMatch:
            return False
        if request.path.rstrip("/") != path.rstrip("/"):
            return False
        if not query:
            return True
        wanted = QueryDict(query)
        for key in wanted:
            if request.GET.get(key) != wanted.get(key):
                return False
        return True

    return active


def _visible_item(entry):
    children = []
    for child in entry.get("items") or []:
        visible = _visible_item(child)
        if visible:
            children.append(visible)
    url_name = entry.get("url_name") or ""
    query = entry.get("query") or ""
    link = _link(url_name, query)
    if link is None and not children:
        return None
    if link is None:
        link = children[0]["link"]
    item = {
        "title": entry["title"],
        "icon": entry.get("icon") or "article",
        "link": link,
    }
    if url_name:
        item["active"] = _active(url_name, query)
    if children:
        item["items"] = children
    return item
