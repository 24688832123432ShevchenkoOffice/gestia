import importlib
from decimal import Decimal

from django.apps import apps
from django.http import QueryDict
from django.test import TestCase
from django.utils import translation

from src.catalog.models import (
    CatalogCell,
    Category,
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductSet,
)
from src.catalog.selectors import filter_catalog, parse_catalog_filters


class FacetTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        self.category = Category.objects.create(slug="cat", name_uk="Каталог")
        style = ProductAttributeGroup.objects.create(slug="style", name_uk="Стиль")
        color = ProductAttributeGroup.objects.create(slug="color", name_uk="Колір")
        self.scandi = ProductAttribute.objects.create(group=style, slug="scandi", name_uk="Скандинавський")
        self.classic = ProductAttribute.objects.create(group=style, slug="classic", name_uk="Класичний")
        self.white = ProductAttribute.objects.create(group=color, slug="white", name_uk="Білий")
        self.green = ProductAttribute.objects.create(group=color, slug="green", name_uk="Зелений")
        self.a = self._product("A", "a", "scandi", "white")
        self.b = self._product("B", "b", "scandi", "green")
        self.c = self._product("C", "c", "classic", "white")

    def _product(self, sku, slug, style, color):
        product = Product.objects.create(
            category=self.category,
            sku=sku,
            slug=slug,
            name_uk=sku,
            price_uah=Decimal("10"),
            price_eur=Decimal("1"),
            stock_qty=100,
        )
        product.filter_attrs.add(
            ProductAttribute.objects.get(slug=style),
            ProductAttribute.objects.get(slug=color),
        )
        return product

    def test_or_inside_group_and_between_groups(self):
        query = QueryDict(mutable=True)
        query.setlist("style", ["scandi", "classic"])
        query.setlist("color", ["white"])
        parsed = parse_catalog_filters(query)
        skus = set(filter_catalog(Product.objects.all(), parsed).values_list("sku", flat=True))
        self.assertEqual(skus, {"A", "C"})

    def test_catalog_mosaic_uses_cell_price_until_filter(self):
        CatalogCell.objects.create(
            product=self.a,
            band=2,
            layout=CatalogCell.Layout.ROW,
            role=CatalogCell.Role.GRID,
            sort=1,
            price_uah=Decimal("8990"),
            crop=CatalogCell.Crop.UKR,
            name_width=127,
        )
        page = self.client.get("/katalog/")
        self.assertContains(page, "8 990 UAH")
        filtered = self.client.get("/katalog/?in_stock=1")
        self.assertNotContains(filtered, "8 990 UAH")
        self.assertContains(filtered, "data-qa=\"product-grid\"")

    def test_category_page_shows_grid_not_mosaic(self):
        CatalogCell.objects.create(
            product=self.a,
            band=1,
            layout=CatalogCell.Layout.ROW,
            role=CatalogCell.Role.GRID,
            sort=1,
            price_uah=Decimal("8990"),
            crop=CatalogCell.Crop.UKR,
            name_width=127,
        )
        other = Category.objects.create(slug="other", name_uk="Інше")
        self.b.category = other
        self.b.save(update_fields=["category"])
        page = self.client.get("/katalog/cat/")
        self.assertContains(page, 'data-qa="product-grid"')
        self.assertNotContains(page, "catalog-row")
        self.assertContains(page, "/tovar/a/")
        self.assertNotContains(page, "/tovar/b/")

    def test_category_narrows_with_style(self):
        other = Category.objects.create(slug="other", name_uk="Інше")
        self.c.category = other
        self.c.save(update_fields=["category"])
        query = QueryDict(mutable=True)
        query.setlist("category", ["cat"])
        query.setlist("style", ["scandi"])
        parsed = parse_catalog_filters(query)
        skus = set(filter_catalog(Product.objects.all(), parsed).values_list("sku", flat=True))
        self.assertEqual(skus, {"A", "B"})

    def test_filter_panel_lists_figma_actions(self):
        page = self.client.get("/katalog/")
        self.assertContains(page, "Застосувати")
        self.assertContains(page, "Скандинавський")
        self.assertContains(page, 'data-catalog-open')
        self.assertContains(page, 'data-catalog-sheet')
        self.assertContains(page, 'data-sheet-open')

    def test_product_page_shows_figma_purchase(self):
        page = self.client.get("/tovar/a/")
        self.assertContains(page, "Додати в кошик")
        self.assertContains(page, "Замовити одразу")
        self.assertContains(page, 'name="qty"')
        self.assertContains(page, 'max="99"')
        self.assertContains(page, "data-qty-label")
        self.assertContains(page, "Арт. A")

    def test_search_keeps_name(self):
        query = QueryDict(mutable=True)
        query["q"] = "A"
        parsed = parse_catalog_filters(query)
        skus = list(filter_catalog(Product.objects.all(), parsed).values_list("sku", flat=True))
        self.assertEqual(skus, ["A"])


class EnglishCatalogCopyTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        self.copy = importlib.import_module("src.catalog.migrations.0009_english_catalog_copy")
        self.category = Category.objects.create(slug="svichky", name_uk="Свічки", name_en="")
        Category.objects.create(slug="tekstyl", name_uk="Текстиль ", name_en="Already translated")
        Category.objects.create(slug="not-in-shop", name_uk="Інше", name_en="")
        ProductSet.objects.create(slug="velykodni", name_uk="Великодній", name_en="")
        style = ProductAttributeGroup.objects.create(slug="style", name_uk="Стиль", name_en="Kept style")
        ProductAttribute.objects.create(group=style, slug="scandi", name_uk="Скандинавський", name_en="")
        self.product = Product.objects.create(
            category=self.category,
            sku="GH-04",
            slug="vesilnyi",
            name_uk="Бокс «Весільний»",
            name_en="",
            price_uah=Decimal("14980.00"),
            price_eur=Decimal("320.00"),
            stock_qty=100,
        )
        Product.objects.create(
            category=self.category,
            sku="GH-01",
            slug="velykodnii-ukrainskyi",
            name_uk="Бокс Великодній «Український»",
            name_en="Custom English name",
            price_uah=Decimal("8990.00"),
            price_eur=Decimal("190.00"),
            stock_qty=100,
        )
        self.nest = Product.objects.create(
            category=self.category,
            sku="TL-0012",
            slug="velykodnii-hnizdo",
            name_uk="Бокс Великодній «Гніздо»",
            description_uk="Великодній бокс «Гніздо» — святкова композиція",
            name_en="",
            description_en="",
            price_uah=Decimal("2450.00"),
            price_eur=Decimal("52.00"),
            stock_qty=100,
        )

    def test_fill_writes_empty_english_and_skips_existing_or_unknown(self):
        self.copy.fill_english_catalog(apps, None)
        self.category.refresh_from_db()
        self.product.refresh_from_db()
        self.nest.refresh_from_db()
        self.assertEqual(self.category.name_en, "Candles")
        self.assertEqual(Category.objects.get(slug="tekstyl").name_en, "Already translated")
        self.assertEqual(Category.objects.get(slug="not-in-shop").name_en, "")
        self.assertEqual(self.product.name_en, "Wedding box")
        self.assertEqual(Product.objects.get(sku="GH-01").name_en, "Custom English name")
        self.assertEqual(self.nest.name_en, "Easter box “The Nest”")
        self.assertIn("flower-shaped candle holders", self.nest.description_en)
        self.assertEqual(ProductAttributeGroup.objects.get(slug="style").name_en, "Kept style")
        self.assertEqual(ProductAttribute.objects.get(slug="scandi").name_en, "Scandinavian")
        self.assertEqual(ProductSet.objects.get(slug="velykodni").name_en, "Easter")

    def test_english_product_page_shows_english_name(self):
        self.copy.fill_english_catalog(apps, None)
        page = self.client.get("/en/tovar/vesilnyi/")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'lang="en"')
        self.assertContains(page, "<h1>Wedding box</h1>")
        self.assertNotContains(page, "Бокс «Весільний»")
        nest = self.client.get("/en/tovar/velykodnii-hnizdo/")
        self.assertContains(nest, "Easter box “The Nest”")
        self.assertContains(nest, "flower-shaped candle holders")
        self.assertNotContains(nest, "Бокс Великодній «Гніздо»")
