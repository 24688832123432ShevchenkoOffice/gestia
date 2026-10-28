"""Транслітерація КМУ 2010 і слаг лише для нових обʼєктів з порожнім полем."""

from __future__ import annotations

from django.utils.text import slugify

_PLAIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "h",
    "ґ": "g",
    "д": "d",
    "е": "e",
    "ж": "zh",
    "з": "z",
    "и": "y",
    "і": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
}
_WORD_START = {"є": "ye", "ї": "yi", "й": "y", "ю": "yu", "я": "ya"}
_WORD_MID = {"є": "ie", "ї": "i", "й": "i", "ю": "iu", "я": "ia"}
_APOSTROPHE = frozenset("'`ʼ’‘′")


def transliterate_uk(value: str) -> str:
    """Кирилиця → латиниця. Апостроф і мʼякий знак не пишуться. зг → zgh."""
    text = value or ""
    out: list[str] = []
    word_start = True
    index = 0
    while index < len(text):
        char = text[index]
        lower = char.lower()
        nxt = text[index + 1].lower() if index + 1 < len(text) else ""
        if lower == "з" and nxt == "г":
            if char.isupper() and text[index + 1].isupper():
                piece = "ZGH"
            elif char.isupper():
                piece = "Zgh"
            else:
                piece = "zgh"
            out.append(piece)
            word_start = False
            index += 2
            continue
        if lower in _WORD_START:
            piece = _WORD_START[lower] if word_start else _WORD_MID[lower]
            out.append(_cased(char, piece))
            word_start = False
            index += 1
            continue
        if lower in _PLAIN:
            out.append(_cased(char, _PLAIN[lower]))
            word_start = False
            index += 1
            continue
        if lower == "ь" or char in _APOSTROPHE:
            index += 1
            continue
        out.append(char)
        word_start = not char.isalpha()
        index += 1
    return "".join(out)


def slugify_uk(value: str, *, max_length: int = 80) -> str:
    base = slugify(transliterate_uk(value))
    if not base:
        return ""
    trimmed = base[:max_length].strip("-")
    return trimmed


def unique_slug(
    model,
    source: str,
    *,
    slug_field: str = "slug",
    max_length: int | None = None,
    instance=None,
    extra_filter: dict | None = None,
) -> str:
    field = model._meta.get_field(slug_field)
    limit = max_length or field.max_length or 50
    base = slugify_uk(source, max_length=limit) or "item"
    candidate = base
    queryset = model._default_manager.all()
    if extra_filter:
        queryset = queryset.filter(**extra_filter)
    number = 2
    while number < 1000:
        conflict = queryset.filter(**{slug_field: candidate})
        if instance is not None and getattr(instance, "pk", None):
            conflict = conflict.exclude(pk=instance.pk)
        if not conflict.exists():
            return candidate
        suffix = f"-{number}"
        head = base[: max(1, limit - len(suffix))].strip("-") or "item"
        if len(head) + len(suffix) > limit:
            head = head[: limit - len(suffix)].strip("-") or "item"
        candidate = f"{head}{suffix}"
        number += 1
    raise ValueError("Не вдалося підібрати унікальний слаг")


def ensure_new_slug(
    instance,
    *,
    source_field: str = "name_uk",
    slug_field: str = "slug",
    extra_filter: dict | None = None,
) -> bool:
    """Заповнює слаг лише в нового обʼєкта, якщо поле порожнє."""
    if getattr(instance, "pk", None):
        return False
    if (getattr(instance, slug_field, "") or "").strip():
        return False
    source = (getattr(instance, source_field, "") or "").strip()
    if not source:
        return False
    setattr(
        instance,
        slug_field,
        unique_slug(
            type(instance),
            source,
            slug_field=slug_field,
            instance=instance,
            extra_filter=extra_filter,
        ),
    )
    return True


def _cased(char: str, piece: str) -> str:
    if not piece or not char.isupper():
        return piece
    return piece[0].upper() + piece[1:]
