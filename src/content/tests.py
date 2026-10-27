from django.test import TestCase
from django.utils import translation


class PublicPageTests(TestCase):
    def test_pages_render(self):
        translation.activate("uk")
        for url in ("/", "/pro-nas/", "/katalog/", "/koshik/", "/polityka-konfidentsiynosti/"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_about_frame_copy(self):
        translation.activate("uk")
        response = self.client.get("/pro-nas/")
        body = response.content.decode()
        self.assertIn(">Головна</a>/<span", body)
        self.assertContains(response, "Наша\u00a0філософія")
        self.assertContains(response, "и\u00a0прагнемо")
        self.assertIn("&#8203;", body)
        self.assertIn("figma/about/imgVideoBanner.png", body)
        self.assertIn("figma/about/imgVideoIcon.svg", body)
        self.assertIn("figma/about/imgGalleryImage1.png", body)
        self.assertNotIn("figma.com/api/mcp/asset", body)
