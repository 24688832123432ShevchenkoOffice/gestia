from django.core.cache import cache
from django.test import TestCase
from django.utils import translation

from src.content.models import SiteSettings


class LanguageTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        cache.clear()
        SiteSettings.objects.update_or_create(pk=1, defaults={"ru_enabled": True, "en_enabled": True})
        cache.clear()

    def test_double_prefix_collapses(self):
        response = self.client.get("/en/ru/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/ru/")

    def test_switch_roundtrip(self):
        response = self.client.post("/i18n/setlang/", {"language": "ru", "next": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/ru/")
        response = self.client.post("/i18n/setlang/", {"language": "uk", "next": "/ru/katalog/"})
        self.assertEqual(response["Location"], "/katalog/")

    def test_disabled_language_redirects_home(self):
        SiteSettings.objects.filter(pk=1).update(ru_enabled=False)
        cache.clear()
        response = self.client.get("/ru/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")
