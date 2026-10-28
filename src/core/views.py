import re

from django.conf import settings
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.i18n import check_for_language

from src.content.models import SiteSettings
from src.core.i18n import collapse_double_prefix, localize_path, safe_next
from src.core.middleware import language_enabled

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def healthz(request):
    return HttpResponse("ok")


def page_not_found(request, exception):
    request.seo_noindex = True
    return render(request, "404.html", status=404)


def robots_txt(request):
    from src.core.seo import robots_text

    return HttpResponse(robots_text(request), content_type="text/plain")


def llms_txt(request):
    from src.core.seo_llms import llms_text

    return HttpResponse(llms_text(request), content_type="text/plain; charset=utf-8")


def llm_txt(request):
    return HttpResponsePermanentRedirect(reverse("llms"))


def theme_css(request):
    site = SiteSettings.load()
    ink = site.color_ink if HEX.match(site.color_ink or "") else "#241c16"
    paper = site.color_paper if HEX.match(site.color_paper or "") else "#f3eee6"
    accent = site.color_accent if HEX.match(site.color_accent or "") else "#8d3b2a"
    css = (
        ":root{"
        f"--ink:{ink};"
        f"--paper:{paper};"
        f"--accent:{accent};"
        "}"
    )
    return HttpResponse(css, content_type="text/css")


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
