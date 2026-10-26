from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models

from src.core.utils import localized

IMAGE_VALIDATOR = FileExtensionValidator(["jpg", "jpeg", "png", "webp"])
VIDEO_VALIDATOR = FileExtensionValidator(["mp4", "webm"])


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self.cache_key)

    @classmethod
    def load(cls):
        cached = cache.get(cls.cache_key)
        if cached is not None:
            return cached
        obj, _created = cls.objects.get_or_create(pk=1)
        cache.set(cls.cache_key, obj, 60)
        return obj


class SiteSettings(SingletonModel):
    cache_key = "site_settings_v1"
    phone = models.CharField("Телефон", max_length=40, default="+380000000000")
    email = models.EmailField("Email", blank=True)
    address_uk = models.CharField("Адреса", max_length=255, blank=True)
    address_ru = models.CharField("Адреса (RU)", max_length=255, blank=True)
    address_en = models.CharField("Адреса (EN)", max_length=255, blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    logo = models.ImageField(
        "Логотип",
        upload_to="site/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
    )
    ru_enabled = models.BooleanField("Російська увімкнена", default=True)
    en_enabled = models.BooleanField("Англійська увімкнена", default=True)
    telegram_notify_orders = models.BooleanField("Telegram: замовлення", default=True)
    telegram_notify_leads = models.BooleanField("Telegram: заявки", default=True)
    color_ink = models.CharField("Колір тексту", max_length=7, default="#241c16")
    color_paper = models.CharField("Колір тла", max_length=7, default="#f3eee6")
    color_accent = models.CharField("Акцент", max_length=7, default="#8d3b2a")
    footer_note_uk = models.CharField("Підпис у підвалі", max_length=255, blank=True)
    footer_note_ru = models.CharField("Підпис у підвалі (RU)", max_length=255, blank=True)
    footer_note_en = models.CharField("Підпис у підвалі (EN)", max_length=255, blank=True)

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return "Налаштування сайту"

    @property
    def address(self):
        return localized(self, "address")

    @property
    def footer_note(self):
        return localized(self, "footer_note")


class HomeBlock(models.Model):
    class Key(models.TextChoices):
        HERO = "hero", "Головний банер"
        CATEGORIES = "categories", "Категорії"
        ADVANTAGES = "advantages", "Переваги"

    key = models.CharField("Ключ", max_length=32, choices=Key.choices, unique=True)
    title_uk = models.CharField("Заголовок", max_length=200)
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    text_uk = models.TextField("Текст", blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    image = models.ImageField(
        "Зображення",
        upload_to="home/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
    )
    video = models.FileField(
        "Відео",
        upload_to="home/video/",
        blank=True,
        validators=[VIDEO_VALIDATOR],
    )
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["sort", "id"]
        verbose_name = "Блок головної"
        verbose_name_plural = "Блоки головної"

    def __str__(self):
        return self.get_key_display()

    @property
    def title(self):
        return localized(self, "title")

    @property
    def text(self):
        return localized(self, "text")


class Advantage(models.Model):
    title_uk = models.CharField("Заголовок", max_length=160)
    title_ru = models.CharField("Заголовок (RU)", max_length=160, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=160, blank=True)
    text_uk = models.TextField("Текст", blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["sort", "id"]
        verbose_name = "Перевага"
        verbose_name_plural = "Переваги"

    def __str__(self):
        return self.title_uk

    @property
    def title(self):
        return localized(self, "title")

    @property
    def text(self):
        return localized(self, "text")


class AboutPage(SingletonModel):
    cache_key = "about_page_v1"
    title_uk = models.CharField("Заголовок", max_length=200, default="Про нас")
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    body_uk = models.TextField("Текст", blank=True)
    body_ru = models.TextField("Текст (RU)", blank=True)
    body_en = models.TextField("Текст (EN)", blank=True)
    image = models.ImageField(
        "Фото",
        upload_to="about/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
    )
    video = models.FileField(
        "Відео",
        upload_to="about/video/",
        blank=True,
        validators=[VIDEO_VALIDATOR],
    )
    seo_title_uk = models.CharField("SEO title", max_length=200, blank=True)
    seo_title_ru = models.CharField("SEO title (RU)", max_length=200, blank=True)
    seo_title_en = models.CharField("SEO title (EN)", max_length=200, blank=True)
    seo_description_uk = models.CharField("SEO description", max_length=300, blank=True)
    seo_description_ru = models.CharField("SEO description (RU)", max_length=300, blank=True)
    seo_description_en = models.CharField("SEO description (EN)", max_length=300, blank=True)

    class Meta:
        verbose_name = "Сторінка «Про нас»"
        verbose_name_plural = "Сторінка «Про нас»"

    def __str__(self):
        return "Про нас"

    @property
    def title(self):
        return localized(self, "title")

    @property
    def body(self):
        return localized(self, "body")

    @property
    def seo_title(self):
        return localized(self, "seo_title") or self.title

    @property
    def seo_description(self):
        return localized(self, "seo_description")


class PrivacyPage(SingletonModel):
    cache_key = "privacy_page_v1"
    title_uk = models.CharField("Заголовок", max_length=200, default="Політика конфіденційності")
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    body_uk = models.TextField("Текст", blank=True)
    body_ru = models.TextField("Текст (RU)", blank=True)
    body_en = models.TextField("Текст (EN)", blank=True)
    seo_title_uk = models.CharField("SEO title", max_length=200, blank=True)
    seo_title_ru = models.CharField("SEO title (RU)", max_length=200, blank=True)
    seo_title_en = models.CharField("SEO title (EN)", max_length=200, blank=True)
    seo_description_uk = models.CharField("SEO description", max_length=300, blank=True)
    seo_description_ru = models.CharField("SEO description (RU)", max_length=300, blank=True)
    seo_description_en = models.CharField("SEO description (EN)", max_length=300, blank=True)

    class Meta:
        verbose_name = "Політика конфіденційності"
        verbose_name_plural = "Політика конфіденційності"

    def __str__(self):
        return "Політика конфіденційності"

    @property
    def title(self):
        return localized(self, "title")

    @property
    def body(self):
        return localized(self, "body")

    @property
    def seo_title(self):
        return localized(self, "seo_title") or self.title

    @property
    def seo_description(self):
        return localized(self, "seo_description")
