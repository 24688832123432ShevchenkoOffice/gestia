from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

PREFIXES = tuple(code for code, _label in settings.LANGUAGES if code != settings.LANGUAGE_CODE)


def _split_query(path: str) -> tuple[str, str]:
    if "?" not in path:
        return path, ""
    bare, query = path.split("?", 1)
    return bare, "?" + query


def strip_language_prefix(path: str) -> str:
    bare, query = _split_query(path or "/")
    parts = bare.split("/")
    while len(parts) > 1 and parts[1] in PREFIXES:
        parts.pop(1)
    result = "/".join(parts) or "/"
    if not result.startswith("/"):
        result = "/" + result
    return result + query


def collapse_double_prefix(path: str) -> str:
    bare, query = _split_query(path or "/")
    parts = bare.split("/")
    while len(parts) > 2 and parts[1] in PREFIXES and parts[2] in PREFIXES:
        parts.pop(1)
    return "/".join(parts) + query


def localize_path(path: str, lang: str) -> str:
    bare, query = _split_query(strip_language_prefix(path or "/"))
    if not bare.startswith("/"):
        bare = "/" + bare
    if lang == settings.LANGUAGE_CODE:
        result = bare or "/"
    elif bare == "/":
        result = f"/{lang}/"
    else:
        result = f"/{lang}{bare}"
    return collapse_double_prefix(result + query)


def safe_next(raw: str) -> str:
    if not raw:
        return "/"
    parts = urlsplit(raw)
    if parts.scheme or parts.netloc:
        return "/"
    path = parts.path or "/"
    if not path.startswith("/") or path.startswith("//"):
        return "/"
    return urlunsplit(("", "", path, parts.query, ""))
