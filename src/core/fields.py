from django.db import models

from src.core.images import convert_fieldfile


class WebPImageField(models.ImageField):
    """ImageField, який сам перетворює новий JPEG/PNG на WebP."""

    def pre_save(self, model_instance, add):
        convert_fieldfile(getattr(model_instance, self.name, None))
        return super().pre_save(model_instance, add)
