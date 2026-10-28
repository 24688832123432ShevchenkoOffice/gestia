"""Спільний вибір: на вітрині або фото, або відео з постером."""

from django.core.validators import FileExtensionValidator
from django.db import models

from src.core.fields import WebPImageField

IMAGE_VALIDATOR = FileExtensionValidator(["jpg", "jpeg", "png", "webp"])
VIDEO_VALIDATOR = FileExtensionValidator(["mp4", "webm"])


class MediaChoice(models.Model):
    class Kind(models.TextChoices):
        PHOTO = "photo", "Фото"
        VIDEO = "video", "Відео"

    media_kind = models.CharField(
        "Що показати",
        max_length=8,
        choices=Kind.choices,
        default=Kind.PHOTO,
        help_text="Фото — картинка. Відео — MP4 або WEBM.",
    )
    poster = WebPImageField(
        "Постер",
        upload_to="posters/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
        help_text="Кадр до старту відео. Якщо порожньо — береться основне фото.",
    )

    class Meta:
        abstract = True

    @property
    def shows_video(self):
        video = getattr(self, "video", None)
        return self.media_kind == self.Kind.VIDEO and bool(video)
