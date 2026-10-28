import re

from src.core.tests_seo import SeoFixture, _meta_description

_SEO_TITLE_UK = "Святкові бокси для сервірування столу"
_SEO_TITLE_EN = "Festive boxes for a table from Gestia"
_SEO_DESC_UK = (
    "Святкові бокси, свічки й текстиль для сервірування святкового столу від Gestia Home."
)
_SEO_DESC_EN = "Festive table boxes, candles and home textiles from Gestia Home."


def _title(response):
    return re.search(r"<title>(.*?)</title>", response.content.decode()).group(1)


class CategorySeoTests(SeoFixture):
    def test_category_meta_uses_translation_or_current_fallback(self):
        path = self.category.get_absolute_url()
        page = self.client.get(path)
        self.assertEqual(_title(page), "Святкові бокси — Gestia")
        self.assertEqual(_meta_description(page), "Святкові бокси. Gestia")

        self.category.seo_title_uk = _SEO_TITLE_UK
        self.category.seo_title_en = _SEO_TITLE_EN
        self.category.seo_description_uk = _SEO_DESC_UK
        self.category.seo_description_en = _SEO_DESC_EN
        self.category.save()

        uk = self.client.get(path)
        en = self.client.get(f"/en{path}")
        self.assertEqual(_title(uk), _SEO_TITLE_UK)
        self.assertEqual(_meta_description(uk), _SEO_DESC_UK)
        self.assertEqual(_title(en), _SEO_TITLE_EN)
        self.assertEqual(_meta_description(en), _SEO_DESC_EN)
        self.assertIn(
            f'<h1 class="visually-hidden">{self.category.name_uk}</h1>',
            uk.content.decode(),
        )

        self.category.seo_title_en = ""
        self.category.seo_description_en = ""
        self.category.save()
        en_fallback = self.client.get(f"/en{path}")
        self.assertEqual(_title(en_fallback), _SEO_TITLE_UK)
        self.assertEqual(_meta_description(en_fallback), _SEO_DESC_UK)

        self.category.seo_title_uk = "   "
        self.category.seo_description_uk = "   "
        self.category.save()
        cleared = self.client.get(f"/en{path}")
        self.assertEqual(_title(cleared), "Festive boxes — Gestia")
        self.assertEqual(_meta_description(cleared), "Festive boxes. Gestia")
