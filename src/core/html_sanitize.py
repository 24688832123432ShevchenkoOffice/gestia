"""Allowlist для форматованого тексту. style і скрипти прибираються."""

from __future__ import annotations

import nh3

ALLOWED_TAGS = frozenset(
    {
        "p",
        "br",
        "strong",
        "em",
        "u",
        "a",
        "ul",
        "ol",
        "li",
        "h2",
        "h3",
        "h4",
        "blockquote",
        "span",
    }
)
ALLOWED_ATTRIBUTES = {"a": frozenset({"href", "target"})}
URL_SCHEMES = frozenset({"http", "https", "mailto"})


def _attribute_value(tag: str, attribute: str, value: str) -> str | None:
    if tag == "a" and attribute == "target":
        return "_blank" if value == "_blank" else None
    return value


def sanitize_rich_html(value: str | None) -> str:
    text = value or ""
    if not text.strip():
        return ""
    cleaned = nh3.clean(
        text,
        tags=set(ALLOWED_TAGS),
        attributes={tag: set(names) for tag, names in ALLOWED_ATTRIBUTES.items()},
        attribute_filter=_attribute_value,
        url_schemes=set(URL_SCHEMES),
        link_rel="noopener noreferrer",
        strip_comments=True,
        generic_attribute_prefixes=set(),
    )
    return cleaned.strip()
