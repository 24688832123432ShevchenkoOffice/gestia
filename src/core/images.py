"""JPEG/PNG → WebP під час збереження нового файлу."""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

QUALITY = 82
MAX_SIDE = 2560
_CONVERT_SUFFIXES = {".jpg", ".jpeg", ".png"}


def encode_upload(uploaded, source_name: str) -> ContentFile | None:
    suffix = Path(source_name or "").suffix.lower()
    if suffix not in _CONVERT_SUFFIXES:
        return None
    if hasattr(uploaded, "seek"):
        uploaded.seek(0)
    try:
        image = Image.open(uploaded)
        image.load()
    except Exception:
        logger.warning("Не вдалося прочитати зображення %s", Path(source_name).name)
        _rewind(uploaded)
        return None
    if (image.format or "").upper() not in {"JPEG", "PNG"}:
        _rewind(uploaded)
        return None
    try:
        image = ImageOps.exif_transpose(image) or image
    except Exception:
        pass
    image = _with_alpha(image)
    if max(image.width, image.height) > MAX_SIDE:
        image.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format="WEBP", quality=QUALITY, method=6)
    stem = Path(source_name).stem or "image"
    return ContentFile(buffer.getvalue(), name=f"{stem}.webp")


def convert_fieldfile(fieldfile) -> None:
    if not fieldfile or getattr(fieldfile, "_committed", True):
        return
    source_name = getattr(fieldfile, "name", "") or ""
    content = None
    try:
        content = encode_upload(fieldfile.file, source_name)
    except Exception:
        logger.warning("Не вдалося конвертувати зображення %s", Path(source_name).name)
        return
    if content is None:
        return
    fieldfile.save(Path(content.name).name, content, save=False)


def convert_images_on_save(sender, instance, **kwargs):
    meta = getattr(instance, "_meta", None)
    if meta is None:
        return
    for field in meta.concrete_fields:
        if isinstance(field, ImageField):
            convert_fieldfile(getattr(instance, field.name, None))


def connect() -> None:
    pre_save.connect(convert_images_on_save, dispatch_uid="gestia.images.webp")


def _with_alpha(image: Image.Image) -> Image.Image:
    if image.mode in {"RGBA", "LA"}:
        return image.convert("RGBA")
    if image.mode == "P" and "transparency" in image.info:
        return image.convert("RGBA")
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def _rewind(uploaded) -> None:
    if hasattr(uploaded, "seek"):
        try:
            uploaded.seek(0)
        except Exception:
            return
