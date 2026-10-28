from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import translation

from src.core.admin_nav import NAV_TREE, build_navigation, iter_nav_entries


class SidebarTreeTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        self.user = User.objects.create_superuser("editor", "editor@example.com", "pass-word-9")
        self.client.force_login(self.user)

    def test_pending_entries_stay_in_the_tree(self):
        keys = {entry["key"] for entry in iter_nav_entries(NAV_TREE)}
        self.assertIn("home_cta", keys)
        self.assertIn("discount", keys)
        self.assertIn("styles", keys)
        self.assertIn("legal_offer", keys)
        self.assertIn("legal_cookies", keys)
        self.assertIn("legal_shipping", keys)
        self.assertIn("legal_privacy", keys)

    def test_navigation_skips_missing_urls(self):
        groups = build_navigation(None)
        titles = [group["title"] for group in groups]
        self.assertIn("Головна", titles)
        self.assertIn("Каталог", titles)
        self.assertIn("Юридичні сторінки", titles)
        self.assertNotIn("Знижка", titles)
        self.assertNotIn("Стилі", titles)
        labels = _labels(groups)
        self.assertIn("Товари", labels)
        self.assertIn("Категорії", labels)
        self.assertIn("Сети", labels)
        self.assertIn("Атрибути", labels)
        self.assertIn("Групи атрибутів", labels)
        self.assertIn("Фрейми каталогу", labels)
        self.assertIn("Політика конфіденційності", labels)
        self.assertNotIn("CTA та контактні форми", labels)
        self.assertNotIn("Публічний договір", labels)

    def test_admin_index_renders_ukrainian_tree(self):
        self.client.cookies["django_language"] = "en"
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestia Home")
        self.assertContains(response, "Головна")
        self.assertContains(response, "Головний банер")
        self.assertContains(response, "key__exact=hero")
        self.assertContains(response, "Про нас")
        self.assertContains(response, "Замовлення і заявки")
        self.assertContains(response, "Хедер і футер")
        self.assertContains(response, "Користувачі")
        self.assertContains(response, "Вийти")
        self.assertNotContains(response, "Знижка")

    def test_user_and_group_changelists_open(self):
        self.assertEqual(self.client.get(reverse("admin:auth_user_changelist")).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:auth_group_changelist")).status_code, 200)


class UserDeleteGuardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("owner", "owner@example.com", "pass-word-9")
        self.admin = admin.site._registry[User]
        self.request = RequestFactory().post("/users/")
        self.request.user = self.user
        self.request.session = SessionStore()
        self.request._messages = FallbackStorage(self.request)

    def test_cannot_delete_self_or_last_superuser(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.user))
        with self.assertRaises(PermissionDenied):
            self.admin.delete_model(self.request, self.user)
        self.admin.delete_queryset(self.request, User.objects.filter(pk=self.user.pk))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_batch_keeps_a_superuser(self):
        other = User.objects.create_superuser("other", "other@example.com", "pass-word-9")
        self.admin.delete_queryset(self.request, User.objects.filter(pk__in=[self.user.pk, other.pk]))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(User.objects.filter(pk=other.pk).exists())


def _labels(groups):
    found = []
    for group in groups:
        for item in group["items"]:
            found.append(item["title"])
            for child in item.get("items") or []:
                found.append(child["title"])
    return found
