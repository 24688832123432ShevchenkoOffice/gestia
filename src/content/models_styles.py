from django.core.cache import cache
from django.db import models
from django.db.utils import OperationalError, ProgrammingError

from src.content.colors import (
    TOKEN_ACCENT,
    TOKEN_INK,
    TOKEN_PAPER,
    normalize_hex,
    validate_hex_color,
)


class HexColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 7)
        super().__init__(*args, **kwargs)
        self.validators.append(validate_hex_color)

    def to_python(self, value):
        value = super().to_python(value)
        if value in (None, ""):
            return ""
        return normalize_hex(value) or value


class PageStyle(models.Model):
    class Key(models.TextChoices):
        GLOBAL = "global", "Увесь сайт"
        HOME = "home", "Головна"
        CATALOG = "catalog", "Каталог"
        PRODUCT = "product", "Товар"
        CART = "cart", "Кошик"
        CHECKOUT = "checkout", "Оформлення"
        ABOUT = "about", "Про нас"
        LEGAL = "legal", "Юридичні"

    page = models.CharField("Сторінка", max_length=16, choices=Key.choices, unique=True)
    background_color = HexColorField("Колір тла", default=TOKEN_PAPER, blank=True)
    text_color = HexColorField("Колір тексту", default=TOKEN_INK, blank=True)
    hover_color = HexColorField("Колір при наведенні", default=TOKEN_ACCENT, blank=True)

    class Meta:
        ordering = ["page"]
        verbose_name = "Стиль сторінки"
        verbose_name_plural = "Стилі сторінок"

    def __str__(self):
        return self.get_page_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.page != self.Key.GLOBAL:
            return
        self._sync_site_settings()

    def _sync_site_settings(self):
        from src.content.models import SiteSettings

        try:
            SiteSettings.objects.filter(pk=1).update(
                color_ink=normalize_hex(self.text_color) or TOKEN_INK,
                color_paper=normalize_hex(self.background_color) or TOKEN_PAPER,
                color_accent=normalize_hex(self.hover_color) or TOKEN_ACCENT,
            )
        except (OperationalError, ProgrammingError):
            return
        cache.delete(SiteSettings.cache_key)


class GlobalPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Увесь сайт"
        verbose_name_plural = "Увесь сайт"


class HomePageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Головна"
        verbose_name_plural = "Головна"


class CatalogPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Каталог"
        verbose_name_plural = "Каталог"


class ProductPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Товар"
        verbose_name_plural = "Товар"


class CartPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Кошик"
        verbose_name_plural = "Кошик"


class CheckoutPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Оформлення"
        verbose_name_plural = "Оформлення"


class AboutPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Про нас"
        verbose_name_plural = "Про нас"


class LegalPageStyle(PageStyle):
    class Meta:
        proxy = True
        verbose_name = "Юридичні"
        verbose_name_plural = "Юридичні"
