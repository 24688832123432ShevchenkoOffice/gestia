import tempfile
from io import BytesIO
from pathlib import Path

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation
from PIL import Image

from src.content.models_discount import DiscountModal, safe_public_link
from src.core.admin_base import AdminImagePreviewWidget
from src.core.fields import WebPImageField


def _png() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (12, 8), (140, 59, 42)).save(buffer, format="PNG")
    return buffer.getvalue()


class DiscountModalTests(TestCase):
    def tearDown(self):
        translation.activate("uk")
    def test_seed_stays_off_and_hidden(self):
        modal = DiscountModal.objects.get(pk=1)
        self.assertFalse(modal.enabled)
        self.assertEqual(modal.delay_seconds, 15)
        self.assertEqual(modal.shows_per_session, 1)
        self.assertEqual(modal.delay_ms, 15000)
        self.assertEqual(modal.show_limit, 1)
        home = self.client.get("/")
        self.assertNotContains(home, "discount-dialog")
        self.assertNotContains(home, "discount-modal.js")
        self.assertNotContains(home, "discount-modal.css")

    def test_enabled_modal_is_accessible_and_localized(self):
        modal = DiscountModal.load()
        modal.enabled = True
        modal.title_uk = "Знижка на сет"
        modal.title_en = "Set offer"
        modal.text_uk = "<p>Лише сьогодні</p><script>alert(1)</script>"
        modal.text_en = "<p>Today only</p>"
        modal.button_uk = "До каталогу"
        modal.button_en = "To the shop"
        modal.link = "/katalog/"
        modal.delay_seconds = 15
        modal.shows_per_session = 1
        modal.save()
        modal.refresh_from_db()
        self.assertNotIn("script", modal.text_uk)
        self.assertIn("<p>", modal.text_uk)

        translation.activate("uk")
        page = self.client.get("/")
        self.assertContains(page, 'id="discount-dialog"')
        self.assertContains(page, 'role="dialog"')
        self.assertContains(page, 'aria-modal="true"')
        self.assertContains(page, 'aria-labelledby="discount-dialog-title"')
        self.assertContains(page, 'aria-describedby="discount-dialog-text"')
        self.assertContains(page, 'aria-label="Закрити"')
        self.assertContains(page, "data-close-dialog")
        self.assertContains(page, 'data-delay-ms="15000"')
        self.assertContains(page, 'data-shows="1"')
        self.assertContains(page, 'data-storage-key="gestia_discount_modal_shows"')
        self.assertContains(page, "Знижка на сет")
        self.assertContains(page, "Лише сьогодні")
        self.assertContains(page, 'href="/katalog/"')
        self.assertContains(page, "discount-modal.js")
        self.assertContains(page, "discount-modal.css")
        self.assertNotContains(page, "<script>alert")
        before_script = page.content.decode().split("discount-modal.js", 1)[0]
        self.assertIn("dialog.js", before_script)
        source = (
            Path(__file__).resolve().parents[1] / "core/static/js/pages/discount-modal.js"
        ).read_text(encoding="utf-8")
        self.assertIn("sessionStorage", source)
        self.assertIn("showModal", source)
        self.assertIn("Escape", source)
        self.assertIn('"Tab"', source)

        translation.activate("en")
        english = self.client.get("/en/")
        self.assertContains(english, "Set offer")
        self.assertContains(english, "Today only")
        self.assertContains(english, "To the shop")
        self.assertContains(english, 'aria-label="Close"')
        self.assertNotContains(english, "Знижка на сет")

    def test_unsafe_link_is_rejected_and_not_rendered(self):
        self.assertEqual(safe_public_link("/katalog/"), "/katalog/")
        self.assertEqual(safe_public_link("https://gestia.example/sale"), "https://gestia.example/sale")
        self.assertEqual(safe_public_link("javascript:alert(1)"), "")
        self.assertEqual(safe_public_link("//evil.example"), "")
        modal = DiscountModal.load()
        modal.link = "javascript:alert(1)"
        with self.assertRaises(ValidationError):
            modal.full_clean()
        modal.link = "https://shop.example/sale"
        modal.button_uk = "Далі"
        modal.enabled = True
        modal.title_uk = "Пропозиція"
        modal.save()
        page = self.client.get("/")
        self.assertContains(page, 'href="https://shop.example/sale"')

    def test_admin_opens_the_single_record(self):
        user = User.objects.create_superuser("discount", "discount@example.com", "pass-word-9")
        self.client.force_login(user)
        modal = DiscountModal.load()
        listing = reverse("admin:content_discountmodal_changelist")
        change = reverse("admin:content_discountmodal_change", args=[modal.pk])
        self.assertRedirects(self.client.get(listing), change)
        form = self.client.get(change)
        self.assertEqual(form.status_code, 200)
        self.assertContains(form, "Українська")
        self.assertContains(form, "English")
        self.assertContains(form, "tinymce")
        self.assertContains(form, "Показувати вікно")
        self.assertContains(form, "2560")
        self.assertContains(form, 'maxlength="80"')
        self.assertContains(form, 'maxlength="40"')
        self.assertContains(form, "Якщо порожньо")
        model_admin = admin.site._registry[DiscountModal]
        self.assertFalse(model_admin.has_add_permission(form.wsgi_request))
        self.assertFalse(model_admin.has_delete_permission(form.wsgi_request, modal))
        admin_form = form.context["adminform"].form
        self.assertIsInstance(admin_form.fields["image"].widget, AdminImagePreviewWidget)

    def test_image_is_stored_as_webp(self):
        self.assertIsInstance(DiscountModal._meta.get_field("image"), WebPImageField)
        with tempfile.TemporaryDirectory() as media:
            with override_settings(MEDIA_ROOT=media):
                modal = DiscountModal.load()
                modal.image = SimpleUploadedFile("offer.png", _png(), content_type="image/png")
                modal.save()
                modal.refresh_from_db()
                self.assertTrue(modal.image.name.endswith(".webp"))
                with Image.open(modal.image.path) as saved:
                    self.assertEqual(saved.format, "WEBP")
