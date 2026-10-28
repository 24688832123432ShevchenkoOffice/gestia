from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.content.media import IMAGE_VALIDATOR
from src.content.models import SingletonModel
from src.core.fields import WebPImageField
from src.core.utils import localized

_LINK_HINT = "Адреса на сайті, наприклад /katalog/."


def safe_public_link(value: str) -> str:
    raw = (value or "").strip()
    if not raw or len(raw) > 300 or "\\" in raw or any(ch in raw for ch in "\r\n\t"):
        return ""
    if raw.startswith("/") and not raw.startswith("//"):
        return raw
    parts = urlsplit(raw)
    if parts.scheme in {"http", "https"} and parts.netloc and not parts.username and not parts.password:
        return raw
    return ""


def validate_public_link(value: str) -> None:
    if value and not safe_public_link(value):
        raise ValidationError("Вкажіть адресу на сайті або посилання http(s).")


class DiscountModal(SingletonModel):
    cache_key = "discount_modal_v1"
    rich_text_fields = ("text_uk", "text_en")

    enabled = models.BooleanField("Показувати вікно", default=False)
    title_uk = models.CharField("Заголовок", max_length=80, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=80, blank=True)
    text_uk = models.TextField("Текст", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    button_uk = models.CharField("Кнопка", max_length=40, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=40, blank=True)
    link = models.CharField(
        "Посилання кнопки",
        max_length=300,
        blank=True,
        validators=[validate_public_link],
        help_text=_LINK_HINT,
    )
    image = WebPImageField(
        "Зображення",
        upload_to="discount/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
        help_text="Необов’язково. JPG або PNG, довша сторона до 2560 px.",
    )
    delay_seconds = models.PositiveSmallIntegerField(
        "Затримка перед показом, с",
        default=15,
        validators=[MinValueValidator(0), MaxValueValidator(600)],
    )
    shows_per_session = models.PositiveSmallIntegerField(
        "Показів за один візит",
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )

    class Meta:
        verbose_name = "Знижка"
        verbose_name_plural = "Знижка"

    def __str__(self):
        return "Знижка"

    def clean(self):
        super().clean()
        self.link = (self.link or "").strip()
        validate_public_link(self.link)

    @property
    def title(self):
        return localized(self, "title")

    @property
    def text(self):
        return localized(self, "text")

    @property
    def button(self):
        return localized(self, "button")

    @property
    def public_url(self) -> str:
        return safe_public_link(self.link)

    @property
    def delay_ms(self) -> int:
        seconds = self.delay_seconds if self.delay_seconds is not None else 15
        return max(0, min(int(seconds), 600)) * 1000

    @property
    def show_limit(self) -> int:
        raw = self.shows_per_session if self.shows_per_session is not None else 1
        return max(0, min(int(raw), 99))
