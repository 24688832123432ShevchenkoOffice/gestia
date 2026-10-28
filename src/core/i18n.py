from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

PREFIXES = tuple(code for code, _label in settings.LANGUAGES if code != settings.LANGUAGE_CODE)
RETIRED_PREFIXES = ("ru",)


def _split_query(path: str) -> tuple[str, str]:
    if "?" not in path:
        return path, ""
    bare, query = path.split("?", 1)
    return bare, "?" + query


def _join_path(parts: list[str], query: str) -> str:
    result = "/".join(parts) or "/"
    if not result.startswith("/"):
        result = "/" + result
    return result + query


def _is_retired(segment: str) -> bool:
    return segment.lower() in RETIRED_PREFIXES


def strip_language_prefix(path: str) -> str:
    bare, query = _split_query(path or "/")
    parts = bare.split("/")
    while len(parts) > 1 and (parts[1] in PREFIXES or _is_retired(parts[1])):
        parts.pop(1)
    return _join_path(parts, query)


def strip_retired_language_prefix(path: str) -> str | None:
    """Drop a leading /ru segment. None when the path is not a retired URL."""
    bare, query = _split_query(path or "/")
    parts = bare.split("/")
    if len(parts) < 2 or not _is_retired(parts[1]):
        return None
    while len(parts) > 1 and _is_retired(parts[1]):
        parts.pop(1)
    return _join_path(parts, query)


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
