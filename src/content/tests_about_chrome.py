from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from src.content.models import AboutPage, SiteSettings


class AboutRenderTests(TestCase):
    def setUp(self):
        cache.clear()
        translation.activate("uk")
        self.page = AboutPage.load()

    def test_model_lead_replaces_the_literal(self):
        self.page.lead_uk = "Короткий рядок"
        self.page.lead_en = "A short line"
        self.page.save()
        page = self.client.get(reverse("about"))
        self.assertContains(page, "Короткий рядок")
        self.assertNotContains(page, "Сучасна жінка може все.")

    def test_empty_lead_falls_back(self):
        self.page.lead_uk = ""
        self.page.lead_en = ""
        self.page.body_uk = ""
        self.page.body_en = ""
        self.page.save()
        page = self.client.get(reverse("about"))
        self.assertContains(page, "Сучасна жінка може все.")
        self.assertContains(page, "Вона будує кар’єру")

    def test_english_story_uses_the_english_field(self):
        page = self.client.get("/en/pro-nas/")
        self.assertContains(page, "A modern woman can do anything.")
        self.assertContains(page, "She builds a career")
        self.assertNotContains(page, "Сучасна жінка може все.")


class HeaderFooterRenderTests(TestCase):
    def setUp(self):
        cache.clear()
        translation.activate("uk")
        self.site = SiteSettings.load()

    def test_nav_label_and_english(self):
        self.site.nav_about_uk = "Історія"
        self.site.nav_about_en = "Story"
        self.site.save()
        self.assertContains(self.client.get("/"), 'class="head-nav__about"')
        self.assertContains(self.client.get("/"), ">Історія</a>")
        english = self.client.get("/en/")
        self.assertContains(english, ">Story</a>")
        self.assertNotContains(english, ">Історія</a>")

    def test_empty_nav_and_credit_fall_back(self):
        self.site.nav_all_uk = ""
        self.site.nav_all_en = ""
        self.site.credit_uk = ""
        self.site.credit_en = ""
        self.site.logo = ""
        self.site.save()
        page = self.client.get("/")
        self.assertContains(page, ">Усі товари</a>")
        self.assertContains(page, "Вітрину зібрано в")
        self.assertContains(page, "figma/desktop/5493c.png")
        english = self.client.get("/en/")
        self.assertContains(english, ">All products</a>")
        self.assertContains(english, "Storefront assembled by")
