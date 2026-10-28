from django.test import TestCase

from src.catalog.models import Category, ProductAttribute, ProductAttributeGroup, ProductSet
from src.core.slug import slugify_uk, transliterate_uk


class UkrainianSlugTests(TestCase):
    def test_official_2010_examples(self):
        self.assertEqual(transliterate_uk("Згорани"), "Zghorany")
        self.assertEqual(transliterate_uk("розгін"), "rozghin")
        self.assertEqual(transliterate_uk("Єнакієве"), "Yenakiieve")
        self.assertEqual(slugify_uk("Київ"), "kyiv")
        self.assertEqual(slugify_uk("Згорани"), "zghorany")
        self.assertEqual(slugify_uk("розгін"), "rozghin")
        self.assertEqual(slugify_uk("Єнакієве"), "yenakiieve")
        self.assertEqual(slugify_uk("п'ять"), "piat")
        self.assertEqual(slugify_uk("зʼїзд"), "zizd")
        self.assertEqual(slugify_uk("Львів"), "lviv")
        self.assertEqual(slugify_uk("Юрій"), "yurii")
        self.assertEqual(slugify_uk("Щастя"), "shchastia")
        self.assertEqual(slugify_uk("йога"), "yoha")
        self.assertEqual(slugify_uk("гай"), "hai")
        self.assertEqual(slugify_uk("Бокс «Весільний»"), "boks-vesilnyi")

    def test_russian_letters_are_not_mapped(self):
        self.assertEqual(slugify_uk("аыб"), "ab")
        self.assertEqual(slugify_uk("ёлка"), "lka")
        self.assertNotIn("yo", transliterate_uk("ёлка"))

    def test_new_objects_get_slug_only_when_empty(self):
        category = Category(name_uk="Згорани")
        category.save()
        self.assertEqual(category.slug, "zghorany")
        category.name_uk = "Київ"
        category.save()
        self.assertEqual(category.slug, "zghorany")

        taken = Category.objects.create(slug="kyiv", name_uk="Інше")
        fresh = Category(name_uk="Київ")
        fresh.save()
        self.assertEqual(fresh.slug, "kyiv-2")
        taken.name_uk = "Львів"
        taken.save()
        self.assertEqual(taken.slug, "kyiv")

    def test_attribute_slug_is_unique_inside_group(self):
        style = ProductAttributeGroup.objects.create(slug="style", name_uk="Стиль")
        color = ProductAttributeGroup.objects.create(slug="color", name_uk="Колір")
        first = ProductAttribute(group=style, name_uk="Білий")
        first.save()
        second = ProductAttribute(group=color, name_uk="Білий")
        second.save()
        self.assertEqual(first.slug, "bilyi")
        self.assertEqual(second.slug, "bilyi")
        duplicate = ProductAttribute(group=style, name_uk="Білий")
        duplicate.save()
        self.assertEqual(duplicate.slug, "bilyi-2")

    def test_product_set_keeps_explicit_slug(self):
        item = ProductSet.objects.create(slug="velykodni", name_uk="Великодній")
        item.name_uk = "Інший набір"
        item.save()
        self.assertEqual(item.slug, "velykodni")
        generated = ProductSet(name_uk="Великодній")
        generated.save()
        self.assertEqual(generated.slug, "velykodnii")
