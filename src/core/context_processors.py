from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

from src.commerce.forms import ContactForm, style_form
from src.core.i18n import localize_path
from src.core.middleware import language_enabled


def shop(request):
    currency = request.session.get("currency", "uah")
    if currency not in {"uah", "eur"}:
        currency = "uah"
    site = None
    home_blocks = {}
    nav_categories = []
    cart_count = 0
    try:
        from src.catalog.selectors import nav_categories as load_nav
        from src.commerce.cart import item_count
        from src.content.models import HomeBlock, SiteSettings

        site = SiteSettings.load()
        home_blocks = {block.key: block for block in HomeBlock.objects.all()}
        nav_categories = list(load_nav())
        cart_count = item_count(request)
    except (OperationalError, ProgrammingError):
        pass
    full = request.get_full_path()
    switch = {
        code: localize_path(full, code)
        for code, _label in settings.LANGUAGES
        if language_enabled(code)
    }
    return {
        "site_settings": site,
        "home_blocks": home_blocks,
        "nav_categories": nav_categories,
        "currency": currency,
        "cart_count": cart_count,
        "lang_switch_urls": switch,
        "contact_form": style_form(ContactForm()),
    }
