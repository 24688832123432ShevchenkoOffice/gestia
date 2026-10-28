"""Canonical, robots, hreflang і Open Graph з наявного вмісту сайту."""

from __future__ import annotations

from html import unescape
from urllib.parse import urlsplit

from django.conf import settings
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.translation import get_language

TITLE_MAX = 60
DESCRIPTION_MAX = 160

NOINDEX_URL_NAMES = frozenset(
    {
        "cart",
        "checkout",
        "thanks",
        "thanks_legacy",
        "wishlist",
        "callback",
        "buy_now",
    }
)
CATALOG_URL_NAMES = frozenset({"catalog", "category"})
PRIVATE_PREFIXES = (
    "/koshik/",
    "/zamovlennia/",
    "/thank-you/",
    "/diakuiemo/",
    "/obrane/",
    "/zayavka/",
    "/zamovyty-odrazu/",
    "/i18n/",
    "/tinymce/",
    "/healthz/",
)
BRAND = "Gestia Home"
PLACEHOLDER_PHONE_DIGITS = "380000000000"


def clip_text(value, limit: int) -> str:
    text = " ".join(unescape(strip_tags(str(value or ""))).split())
    if len(text) <= limit:
        return text
    trimmed = text[:limit].rstrip()
    if " " in trimmed:
        word = trimmed.rsplit(" ", 1)[0].rstrip()
        if len(word) >= int(limit * 0.6):
            trimmed = word
    return trimmed.rstrip(" .,;:—-–")


def configured_origin() -> tuple[str, str] | None:
    raw = str(getattr(settings, "SITE_URL", "") or "").strip()
    if not raw:
        return None
    if "://" not in raw:
        raw = "https://" + raw.lstrip("/")
    parts = urlsplit(raw)
    if not parts.netloc:
        return None
    return (parts.scheme or "https", parts.netloc)


def public_base(request) -> str:
    origin = configured_origin()
    if origin is not None:
        scheme, netloc = origin
        return f"{scheme}://{netloc}"
    return f"{request.scheme}://{request.get_host()}"


def absolute_media(request, url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    if not value.startswith("/"):
        value = "/" + value
    return public_base(request) + value


def _language() -> str:
    return (get_language() or settings.LANGUAGE_CODE).split("-")[0]


def _language_enabled(code: str) -> bool:
    from src.core.middleware import language_enabled

    return language_enabled(code)


def _url_name(request) -> str:
    match = getattr(request, "resolver_match", None)
    if match is None:
        return ""
    return match.url_name or ""


def _page_number(raw) -> int | None:
    text = str(raw or "").strip()
    if not text.isdigit():
        return None
    number = int(text)
    if number < 1:
        return None
    return number


def _is_tracking(key: str) -> bool:
    return key == "utm" or key.startswith("utm_")


def _query_parts(request):
    page = _page_number(request.GET.get("page")) if "page" in request.GET else None
    extras = []
    for key in request.GET.keys():
        if key == "page" and page is not None:
            continue
        if _is_tracking(key):
            continue
        extras.append(key)
    return page, extras


def _indexable(request, url_name: str, extras: list[str]) -> bool:
    if getattr(request, "seo_noindex", False):
        return False
    if getattr(request, "resolver_match", None) is None:
        return False
    if url_name in NOINDEX_URL_NAMES:
        return False
    if url_name in CATALOG_URL_NAMES and extras:
        return False
    return True


def _canonical_query(indexable: bool, page: int | None) -> str:
    if indexable and page and page > 1:
        return f"?page={page}"
    return ""


def build_head(request, site=None) -> dict:
    url_name = _url_name(request)
    page, extras = _query_parts(request)
    indexable = _indexable(request, url_name, extras)
    query = _canonical_query(indexable, page)
    canonical = public_base(request) + request.path + query
    robots = "" if indexable else "noindex,follow"
    return {
        "canonical": canonical,
        "robots": robots,
        "alternates": _alternates(request, query) if indexable else [],
        "og_type": "product" if url_name == "product" else "website",
        "og_locale": "en_US" if _language() == "en" else "uk_UA",
        "image": _default_image(request, site),
        "indexable": indexable,
    }


def _alternates(request, query: str) -> list[dict]:
    from src.core.i18n import localize_path

    base = public_base(request)
    full = request.path + query
    links = []
    default_href = ""
    for code, _label in settings.LANGUAGES:
        if not _language_enabled(code):
            continue
        href = base + localize_path(full, code)
        links.append({"code": code, "href": href})
        if code == settings.LANGUAGE_CODE:
            default_href = href
    if default_href:
        links.append({"code": "x-default", "href": default_href})
    return links


def _default_image(request, site) -> str:
    logo = getattr(site, "logo", None) if site is not None else None
    if logo:
        try:
            return absolute_media(request, logo.url)
        except ValueError:
            pass
    return absolute_media(request, static("figma/desktop/5493c.png"))


def og_image_url(context) -> str:
    request = context.get("request")
    if request is None:
        return ""
    product = context.get("product")
    cover = getattr(product, "cover", None) if product is not None else None
    image = getattr(cover, "image", None) if cover is not None else None
    if image:
        try:
            return absolute_media(request, image.url)
        except ValueError:
            pass
    seo = context.get("seo") or {}
    return seo.get("image") or ""


def robots_text(request) -> str:
    from src.catalog.selectors import catalog_filter_query_names

    lines = ["User-agent: *", "Allow: /"]
    for prefix in PRIVATE_PREFIXES:
        lines.append(f"Disallow: {prefix}")
    for code, _label in settings.LANGUAGES:
        if code == settings.LANGUAGE_CODE:
            continue
        for prefix in PRIVATE_PREFIXES:
            lines.append(f"Disallow: /{code}{prefix}")
    for key in catalog_filter_query_names():
        lines.append(f"Disallow: /*?*{key}=")
    lines.append("Disallow: /*?*utm_")
    lines.append("")
    lines.append(f"Sitemap: {public_base(request)}/sitemap.xml")
    return "\n".join(lines) + "\n"


def public_contacts() -> tuple[str, str]:
    try:
        from django.db.utils import OperationalError, ProgrammingError

        from src.content.models import SiteSettings

        site = SiteSettings.load()
    except (OperationalError, ProgrammingError, AttributeError):
        return "", ""
    phone = " ".join(str(site.phone or "").split())
    digits = "".join(ch for ch in phone if ch.isdigit())
    if not digits or digits == PLACEHOLDER_PHONE_DIGITS:
        phone = ""
    email = str(site.email or "").strip()
    return phone, email
