from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import translation

from src.content.models import SiteSettings


class LanguageTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        cache.clear()
        SiteSettings.objects.update_or_create(pk=1, defaults={"ru_enabled": False, "en_enabled": True})
        cache.clear()

    def test_double_prefix_collapses(self):
        response = self.client.get("/en/en/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/en/")

    def test_switch_roundtrip(self):
        response = self.client.post("/i18n/setlang/", {"language": "en", "next": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/en/")
        response = self.client.post("/i18n/setlang/", {"language": "uk", "next": "/en/katalog/"})
        self.assertEqual(response["Location"], "/katalog/")

    def test_currency_keeps_language(self):
        session = self.client.session
        session["currency"] = "uah"
        session.save()
        self.client.cookies.load({})
        self.client.post("/i18n/setlang/", {"language": "en", "next": "/katalog/"})
        response = self.client.post(
            "/i18n/setcurrency/",
            {"currency": "eur", "next": "/en/katalog/"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/en/katalog/")
        self.assertEqual(self.client.session.get("currency"), "eur")

    def test_ru_prefix_not_in_languages(self):
        response = self.client.get("/ru/")
        self.assertIn(response.status_code, {302, 404})

    def test_disabled_english_redirects_home(self):
        SiteSettings.objects.filter(pk=1).update(en_enabled=False)
        cache.clear()
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")


class NotFoundTests(TestCase):
    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/no-such-gestia-page/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Сторінку не знайдено", status_code=404)
        self.assertContains(response, "На головну", status_code=404)
        self.assertContains(response, "css/pages/utility.css", status_code=404)
