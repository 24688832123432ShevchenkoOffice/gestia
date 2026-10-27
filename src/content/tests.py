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
        self.assertIn("figma/about/e6ffe24a-dab5-4cc2-8155-190e3c001158.png", body)
        self.assertIn("figma/about/fe172e1f-21be-4583-9078-519fd841cb25.svg", body)
        self.assertIn("figma/about/a525d82b-e09d-4310-8f4a-19715ec6c1f5.png", body)
        self.assertIn("figma/about/m/1c65c9d9-7443-4409-aeec-78269a2a6038.png", body)
        self.assertIn("figma/about/m/fccc8521-cf11-462b-85fa-e0d07c703f08.png", body)
        self.assertIn("figma/about/m/65445179-2967-4089-8231-e953ba0592e1.svg", body)
        self.assertIn("figma/about/m/0bb23f7c-e2ab-4658-a731-ca841f4df6c2.svg", body)
        self.assertIn("data-about-pop", body)
        self.assertIn("Inter:wght@100;400;500", body)
        self.assertIn("флористики", body)
        self.assertNotIn("figma.com/api/mcp/asset", body)
