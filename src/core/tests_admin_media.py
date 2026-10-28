import tempfile
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from src.catalog.models import Category, Product
from src.core.admin_base import IMAGE_HELP
from src.core.fields import WebPImageField
from src.core.images import MAX_SIDE


class WebPAndAdminMediaTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.media = override_settings(MEDIA_ROOT=self.tmp.name)
        self.media.enable()
        self.user = User.objects.create_superuser("media", "media@example.com", "pass-word-9")
        self.client.force_login(self.user)

    def tearDown(self):
        self.media.disable()
        self.tmp.cleanup()

    def test_jpeg_and_png_become_webp_with_alpha_and_max_side(self):
        category = Category(name_uk="Фото", slug="foto")
        category.image = _upload(_image_bytes("JPEG", (20, 10)), "shot.jpg", "image/jpeg")
        category.save()
        self.assertTrue(category.image.name.endswith(".webp"))
        with Image.open(category.image.path) as saved:
            self.assertEqual(saved.format, "WEBP")

        wide = Category(name_uk="Широке", slug="shyroke")
        wide.image = _upload(_image_bytes("PNG", (3000, 10), "RGBA"), "wide.png", "image/png")
        wide.save()
        with Image.open(wide.image.path) as saved:
            self.assertEqual(saved.format, "WEBP")
            self.assertEqual(saved.mode, "RGBA")
            self.assertLessEqual(max(saved.size), MAX_SIDE)
            self.assertEqual(saved.size[0], MAX_SIDE)

        before = Path(category.image.path).read_bytes()
        category.name_uk = "Інша"
        category.save()
        category.refresh_from_db()
        self.assertEqual(Path(category.image.path).read_bytes(), before)

    def test_webp_and_gif_are_not_reencoded(self):
        category = Category(name_uk="Веб", slug="web")
        category.image = _upload(_image_bytes("WEBP", (6, 6)), "keep.webp", "image/webp")
        category.save()
        self.assertTrue(category.image.name.endswith(".webp"))
        stored = Path(category.image.path).read_bytes()

        gif = Category(name_uk="Гіф", slug="gif")
        gif.image = _upload(_image_bytes("GIF", (4, 4)), "anim.gif", "image/gif")
        gif.save()
        self.assertTrue(gif.image.name.endswith(".gif"))
        self.assertNotEqual(Path(category.image.path).read_bytes(), b"")
        self.assertEqual(Path(category.image.path).read_bytes(), stored)

    def test_new_category_form_builds_slug_and_existing_is_readonly(self):
        add_url = reverse("admin:catalog_category_add")
        page = self.client.get(add_url)
        self.assertContains(page, 'name="slug"')
        self.assertContains(page, 'maxlength="160"')
        self.assertContains(page, "char_counter.js")
        self.assertContains(page, "char_counter.css")
        self.assertContains(page, IMAGE_HELP)
        created = self.client.post(
            add_url,
            {"name_uk": "Згорани", "name_en": "", "slug": "", "sort": "0", "is_active": "on"},
        )
        self.assertEqual(created.status_code, 302, getattr(created, "context_data", None))
        self.assertTrue(Category.objects.filter(slug="zghorany").exists())

        category = Category.objects.create(slug="kyiv", name_uk="Київ")
        category.image = _upload(_image_bytes("PNG", (12, 8), "RGB"), "card.png", "image/png")
        category.save()
        change = self.client.get(reverse("admin:catalog_category_change", args=[category.pk]))
        self.assertContains(change, "gestia-admin-thumb")
        self.assertNotContains(change, 'name="slug"')
        self.assertContains(change, "kyiv")
        home = self.client.get("/")
        self.assertNotContains(home, "char_counter.js")

    def test_product_slug_stays_when_renamed(self):
        category = Category.objects.create(slug="cat", name_uk="Каталог")
        product = Product(
            category=category,
            sku="BOX",
            name_uk="Бокс «Весільний»",
            price_uah=Decimal("10"),
            price_eur=Decimal("1"),
            stock_qty=1,
        )
        product.save()
        self.assertEqual(product.slug, "boks-vesilnyi")
        product.name_uk = "Інша назва"
        product.save()
        self.assertEqual(product.slug, "boks-vesilnyi")
        self.assertTrue(issubclass(WebPImageField, models.ImageField))


def _image_bytes(fmt, size, mode="RGB"):
    color = (200, 20, 20, 128) if mode == "RGBA" else (200, 20, 20)
    image = Image.new(mode, size, color)
    buffer = BytesIO()
    image.save(buffer, format=fmt)
    return buffer.getvalue()


def _upload(payload, name, content_type):
    return SimpleUploadedFile(name, payload, content_type=content_type)
