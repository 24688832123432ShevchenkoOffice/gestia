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

    def test_categories_form_keeps_the_video_files(self):
        categories = _block("categories", title_uk="Секція", sort=2)
        video = _block(
            "video",
            media_kind="photo",
            sort=3,
            image="home/video-figma.webp",
            image_mobile="home/video-m.webp",
        )
        url = reverse("admin:content_homecategoriesblock_change", args=[categories.pk])
        before = HomeBlock.objects.filter(key="video").count()
        page = self.client.get(url)
        self.assertEqual(HomeBlock.objects.filter(key="video").count(), before)
        self.assertContains(page, "Відео-блок після категорій")
        self.assertContains(page, "перед популярними товарами")
        self.assertContains(page, "home/video-figma.webp")
        response = self.client.post(
            url,
            {
                "title_uk": "Після правки",
                "title_en": "After",
                "page_video_media_kind": "video",
                "_save": "1",
            },
        )
        self._assert_saved(response)
        categories.refresh_from_db()
        video.refresh_from_db()
        self.assertEqual(categories.title_uk, "Після правки")
        self.assertEqual(video.media_kind, "video")
        self.assertEqual(video.image.name, "home/video-figma.webp")
        self.assertEqual(video.image_mobile.name, "home/video-m.webp")
        self.assertEqual(video.sort, 3)
        self.assertEqual(HomeBlock.objects.filter(key="video").count(), 1)
        self.assertContains(self.client.get("/"), "home/video-figma.webp")

    def test_advantages_form_keeps_both_images(self):
        advantages = _block("advantages", title_uk="Чому ми", sort=5, image="home/card.webp")
        video = _block(
            "video_2",
            media_kind="photo",
            sort=6,
            image="home/video_2-figma.webp",
        )
        url = reverse("admin:content_homeadvantagesblock_change", args=[advantages.pk])
        page = self.client.get(url)
        self.assertContains(page, "Відео-блок після переваг")
        self.assertContains(page, "перед відгуками")
        self.assertContains(page, "home/video_2-figma.webp")
        self.assertContains(page, "home/card.webp")
        response = self.client.post(
            url,
            {
                "title_uk": "Чому Gestia",
                "title_en": "",
                "text_uk": "",
                "text_en": "",
                "text_mobile_uk": "",
                "text_mobile_en": "",
                "cta_uk": "",
                "cta_en": "",
                "page_video_media_kind": "photo",
                "_save": "1",
            },
        )
        self._assert_saved(response)
        advantages.refresh_from_db()
        video.refresh_from_db()
        self.assertEqual(advantages.title_uk, "Чому Gestia")
        self.assertEqual(advantages.image.name, "home/card.webp")
        self.assertEqual(video.image.name, "home/video_2-figma.webp")
        self.assertEqual(video.media_kind, "photo")
        self.assertEqual(HomeBlock.objects.filter(key="video_2").count(), 1)

    def _assert_saved(self, response):
        if response.status_code == 302:
            return
        form = response.context["adminform"].form
        self.fail(form.errors.as_text())


def _block(key, **values):
    block, _created = HomeBlock.objects.get_or_create(key=key, defaults=values)
    for name, value in values.items():
        setattr(block, name, value)
    block.save()
    return block
