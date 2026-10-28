import re

from django.db.utils import OperationalError, ProgrammingError

from src.content.colors import TOKEN_ACCENT, TOKEN_INK, TOKEN_PAPER, normalize_hex

_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")

URL_PAGE = {
    "home": "home",
    "catalog": "catalog",
    "category": "catalog",
    "product": "product",
    "cart": "cart",
    "checkout": "checkout",
    "about": "about",
    "privacy": "legal",
    "offer": "legal",
    "cookies": "legal",
    "shipping": "legal",
}

_PAGE_KEYS = frozenset(URL_PAGE.values())


def page_style_key(request) -> str:
    match = getattr(request, "resolver_match", None)
    name = getattr(match, "url_name", "") if match else ""
    return URL_PAGE.get(name or "", "")


def _site_color(value: str | None, fallback: str) -> str:
    raw = value or ""
    if _HEX.match(raw):
        return raw
    return fallback


def _override(value: str | None, root: str, token: str) -> str:
    color = normalize_hex(value)
    if not color or color == token or color == root.lower():
        return ""
    return color


def build_theme_css() -> str:
    from src.content.models import SiteSettings

    site = SiteSettings.load()
    ink = _site_color(site.color_ink, TOKEN_INK)
    paper = _site_color(site.color_paper, TOKEN_PAPER)
    accent = _site_color(site.color_accent, TOKEN_ACCENT)
    if accent.lower() == TOKEN_ACCENT:
        css = f":root{{--ink:{ink};--paper:{paper};--accent:{accent};}}"
    else:
        css = (
            f":root{{--ink:{ink};--paper:{paper};--accent:{accent};--hover:{accent.lower()};}}"
            "body a:hover,body button:hover{color:var(--hover)}"
        )
    return css + _page_rules(ink, paper, accent)


def _page_rules(ink: str, paper: str, accent: str) -> str:
    from src.content.models_styles import PageStyle

    try:
        rows = list(PageStyle.objects.exclude(page=PageStyle.Key.GLOBAL))
    except (OperationalError, ProgrammingError):
        return ""
    chunks = []
    for row in rows:
        if row.page not in _PAGE_KEYS:
            continue
        decls = []
        background = _override(row.background_color, paper, TOKEN_PAPER)
        text = _override(row.text_color, ink, TOKEN_INK)
        hover = _override(row.hover_color, accent, TOKEN_ACCENT)
        if background:
            decls.append(f"--paper:{background}")
        if text:
            decls.append(f"--ink:{text}")
        if hover:
            decls.append(f"--accent:{hover}")
            decls.append(f"--hover:{hover}")
        if not decls:
            continue
        chunks.append(f'body[data-page="{row.page}"]{{{";".join(decls)};}}')
        if hover:
            chunks.append(
                f'body[data-page="{row.page}"] a:hover,body[data-page="{row.page}"] button:hover{{color:var(--hover)}}'
            )
    return "".join(chunks)
