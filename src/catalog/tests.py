from decimal import Decimal

from django.http import QueryDict
from django.test import TestCase
from django.utils import translation

from src.catalog.models import Category, Product, ProductAttribute, ProductAttributeGroup
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

    def test_search_keeps_name(self):
        query = QueryDict(mutable=True)
        query["q"] = "A"
        parsed = parse_catalog_filters(query)
        skus = list(filter_catalog(Product.objects.all(), parsed).values_list("sku", flat=True))
        self.assertEqual(skus, ["A"])
