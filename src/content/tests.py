from django.test import TestCase
from django.utils import translation


class PublicPageTests(TestCase):
    def test_pages_render(self):
        translation.activate("uk")
        for url in ("/", "/pro-nas/", "/katalog/", "/koshik/", "/polityka-konfidentsiynosti/"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)
