from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from src.content.admin_blocks import HomeCallbackForm
from src.content.literals import LITERALS
from src.content.models import ContactForms, HomeBlock


class HomeBlockRenderTests(TestCase):
    def setUp(self):
        cache.clear()
        translation.activate("uk")

    def test_model_title_replaces_the_literal(self):
        HomeBlock.objects.create(key="popular", title_uk="Наша добірка", title_en="Our edit", sort=3)
        page = self.client.get("/")
        self.assertContains(page, "Наша добірка")
        self.assertNotContains(page, "Популярні товари")

    def test_empty_title_falls_back_to_the_current_copy(self):
        HomeBlock.objects.create(key="popular", title_uk="", title_en="", cta_uk="", cta_en="", sort=3)
        page = self.client.get("/")
        self.assertContains(page, "Популярні товари")
        self.assertContains(page, "Перейти до каталогу")

    def test_english_block_uses_the_english_field(self):
        HomeBlock.objects.create(key="reviews", title_uk="Відгуки", title_en="Guest notes", sort=6)
        page = self.client.get("/en/")
        self.assertContains(page, "Guest notes")
        self.assertNotContains(page, ">Відгуки<")


class ContactFormCopyTests(TestCase):
    def setUp(self):
        cache.clear()
        translation.activate("uk")

    def test_waitlist_title_and_english_fallback(self):
        copy = ContactForms.load()
        copy.waitlist_title_uk = "Майже готово"
        copy.waitlist_title_en = "Almost ready"
        copy.save()
        self.assertContains(self.client.get("/"), "Майже готово")
        self.assertNotContains(self.client.get("/"), LITERALS["waitlist_title"][0])
        english = self.client.get("/en/")
        self.assertContains(english, "Almost ready")
        self.assertContains(english, "adding the final touches to the Gestia Home festive boxes")

    def test_empty_waitlist_uses_the_literal(self):
        copy = ContactForms.load()
        copy.waitlist_button_uk = ""
        copy.waitlist_button_en = ""
        copy.save()
        self.assertContains(self.client.get("/"), "Повідомити мене")
        self.assertContains(self.client.get("/en/"), "Notify me")


class HomeBlockAdminTests(TestCase):
    def setUp(self):
        cache.clear()
        user = User.objects.create_superuser("editor", "editor@example.com", "pass-word-9")
        self.client.force_login(user)
        HomeBlock.objects.create(key="hero", title_uk="Банер тест", sort=1)
        HomeBlock.objects.create(
            key="callback",
            lines_uk="Ім’я\nНомер телефону\nПовідомлення",
            lines_en="Name\nPhone number\nMessage",
            sort=8,
        )

    def test_hero_changelist_opens_the_single_record(self):
        hero = HomeBlock.objects.get(key="hero")
        response = self.client.get(reverse("admin:content_homeheroblock_changelist"))
        self.assertRedirects(response, reverse("admin:content_homeheroblock_change", args=[hero.pk]))
        page = self.client.get(reverse("admin:content_homeheroblock_change", args=[hero.pk]))
        self.assertContains(page, "Банер тест")
        self.assertContains(page, 'maxlength="64"')
        self.assertContains(page, "Виберіть файл для завантаження")
        self.assertNotContains(page, "Choose file to upload")

    def test_callback_placeholders_roundtrip(self):
        block = HomeBlock.objects.get(key="callback")
        page = self.client.get(reverse("admin:content_homecallbackblock_change", args=[block.pk]))
        self.assertContains(page, "Номер телефону")
        form = HomeCallbackForm(instance=block)
        data = {name: form[name].value() if form[name].value() is not None else "" for name in form.fields}
        bound = HomeCallbackForm(data, instance=block)
        self.assertTrue(bound.is_valid(), bound.errors)
        bound.save()
        self.assertEqual(block.lines_uk, "Ім’я\nНомер телефону\nПовідомлення")
        self.assertEqual(block.lines_en, "Name\nPhone number\nMessage")
