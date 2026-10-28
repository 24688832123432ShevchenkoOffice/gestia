from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from django.http import HttpResponseRedirect
from django.utils import translation

from src.core.i18n import collapse_double_prefix, localize_path


def language_enabled(lang: str) -> bool:
    allowed = {code for code, _label in settings.LANGUAGES}
    if lang not in allowed:
        return False
    if lang == settings.LANGUAGE_CODE:
        return True
    try:
        from src.content.models import SiteSettings

        site = SiteSettings.load()
    except (OperationalError, ProgrammingError):
        return True
    if lang == "en":
        return site.en_enabled
    return False


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy = getattr(settings, "CSP_POLICY", "") or ""
        if not policy:
            return response
        header = (
            "Content-Security-Policy-Report-Only"
            if getattr(settings, "CSP_REPORT_ONLY", True)
            else "Content-Security-Policy"
        )
        response[header] = policy
        return response


class LanguagePrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        collapsed = collapse_double_prefix(request.path_info)
        if collapsed != request.path_info:
            query = request.META.get("QUERY_STRING", "")
            target = collapsed if not query else f"{collapsed}?{query}"
            return HttpResponseRedirect(target)
        lang = translation.get_language() or settings.LANGUAGE_CODE
        lang = lang.split("-")[0]
        if not language_enabled(lang):
            query = request.META.get("QUERY_STRING", "")
            target = localize_path(request.get_full_path(), settings.LANGUAGE_CODE)
            if query and "?" not in target:
                target = f"{target}?{query}"
            return HttpResponseRedirect(target)
        return self.get_response(request)
