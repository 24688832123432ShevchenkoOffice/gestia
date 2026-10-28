from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.i18n import check_for_language

from src.content.theme import build_theme_css
from src.core.i18n import collapse_double_prefix, localize_path, safe_next
from src.core.middleware import language_enabled


def healthz(request):
    return HttpResponse("ok")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    lines = ["User-agent: *", "Allow: /", "", f"Sitemap: {sitemap_url}"]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def theme_css(request):
    return HttpResponse(build_theme_css(), content_type="text/css")


def _extract_next(request) -> str:
    raw = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(
        raw,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        raw = safe_next(raw)
    else:
        raw = safe_next(raw)
    return raw


@require_POST
def set_language(request):
    lang = request.POST.get("language", "")
    if not check_for_language(lang) or not language_enabled(lang):
        lang = settings.LANGUAGE_CODE
    target = collapse_double_prefix(localize_path(_extract_next(request), lang))
    response = HttpResponseRedirect(target)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response


@require_POST
def set_currency(request):
    currency = request.POST.get("currency", "uah")
    if currency not in {"uah", "eur"}:
        currency = "uah"
    request.session["currency"] = currency
    # Currency only — never touches language cookie / URL prefix.
    target = safe_next(request.POST.get("next") or "/")
    return HttpResponseRedirect(target)
