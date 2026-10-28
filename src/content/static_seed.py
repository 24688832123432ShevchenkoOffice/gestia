"""Копія поточного файлу зі static у media без перекодування."""

from django.contrib.staticfiles.finders import find
from django.core.files.base import File
from django.core.files.storage import default_storage


def place_static(static_rel, stored_name):
    source = find(static_rel)
    if not source:
        return ""
    if not default_storage.exists(stored_name):
        with open(source, "rb") as handle:
            default_storage.save(stored_name, File(handle))
    return stored_name
