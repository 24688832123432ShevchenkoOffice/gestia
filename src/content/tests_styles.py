from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from src.catalog.models import Category, Product
from src.content.colors import TOKEN_ACCENT, TOKEN_INK, TOKEN_PAPER
from src.content.models import SiteSettings
from src.content.models_styles import PageStyle
from src.core.admin_nav import build_navigation


ROOT = ":root{--ink:#241c16;--paper:#f3eee6;--accent:#8d3b2a;}"


class PageStyleTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_seed_matches_tokens_and_theme_stays_exact(self):
        self.assertEqual(PageStyle.objects.count(), 8)
        for row in PageStyle.objects.all():
            self.assertEqual(row.background_color, TOKEN_PAPER)
            self.assertEqual(row.text_color, TOKEN_INK)
            self.assertEqual(row.hover_color, TOKEN_ACCENT)
        css = self.client.get(reverse("theme_css"))
        self.assertEqual(css["Content-Type"], "text/css")
        self.assertEqual(css.content.decode(), ROOT)

    def test_page_override_emits_only_the_changed_color(self):
        row = PageStyle.objects.get(page=PageStyle.Key.CATALOG)
        row.background_color = "#112233"
        row.save()
        css = self.client.get(reverse("theme_css")).content.decode()
        self.assertTrue(css.startswith(ROOT))
        self.assertIn('body[data-page="catalog"]{--paper:#112233;}', css)
        self.assertNotIn('body[data-page="home"]', css)
        self.assertNotIn("--hover:", css)

        row.background_color = TOKEN_PAPER
        row.hover_color = "#123456"
        row.save()
        css = self.client.get(reverse("theme_css")).content.decode()
        self.assertIn(
            'body[data-page="catalog"]{--accent:#123456;--hover:#123456;}',
            css,
        )
        self.assertIn(
            'body[data-page="catalog"] a:hover,body[data-page="catalog"] button:hover{color:var(--hover)}',
            css,
        )
        self.assertNotIn('body[data-page="catalog"]{--paper:', css)

    def test_global_style_updates_site_settings_and_root(self):
        row = PageStyle.objects.get(page=PageStyle.Key.GLOBAL)
        row.hover_color = "#abcdef"
        row.save()
        site = SiteSettings.load()
        self.assertEqual(site.color_accent, "#abcdef")
        css = self.client.get(reverse("theme_css")).content.decode()
        self.assertIn("--accent:#abcdef", css)
        self.assertIn("--hover:#abcdef", css)
        self.assertIn("body a:hover,body button:hover{color:var(--hover)}", css)
        self.assertNotIn('body[data-page=', css)

    def test_site_settings_color_updates_the_global_row(self):
        site = SiteSettings.load()
        site.color_ink = "#222222"
        site.save()
        row = PageStyle.objects.get(page=PageStyle.Key.GLOBAL)
        self.assertEqual(row.text_color, "#222222")
        css = self.client.get(reverse("theme_css")).content.decode()
        self.assertIn("--ink:#222222", css)
        self.assertNotIn('body[data-page=', css)

    def test_invalid_hex_is_rejected_and_bad_site_color_falls_back(self):
        row = PageStyle.objects.get(page=PageStyle.Key.HOME)
        row.background_color = "blue"
        with self.assertRaises(ValidationError):
            row.full_clean()
        row.background_color = "#abc"
        row.full_clean()
        self.assertEqual(row.background_color, "#aabbcc")

        site = SiteSettings.load()
        site.color_paper = "paper"
        site.save()
        css = self.client.get(reverse("theme_css")).content.decode()
        self.assertIn("--paper:#f3eee6", css)

    def test_pages_expose_their_style_key(self):
        category = Category.objects.create(name_uk="Стилі", slug="styli-test")
        product = Product.objects.create(
            category=category,
            sku="STYLE-1",
            slug="style-1",
            name_uk="Стіл",
            price_uah=Decimal("10.00"),
            price_eur=Decimal("1.00"),
            stock_qty=3,
        )
        expected = {
            "/": "home",
            "/en/": "home",
            reverse("catalog"): "catalog",
            reverse("category", kwargs={"slug": category.slug}): "catalog",
            reverse("product", kwargs={"slug": product.slug}): "product",
            reverse("cart"): "cart",
            reverse("about"): "about",
            reverse("offer"): "legal",
            reverse("privacy"): "legal",
            reverse("cookies"): "legal",
            reverse("shipping"): "legal",
            reverse("wishlist"): "",
            reverse("thanks"): "",
        }
        for path, key in expected.items():
            page = self.client.get(path)
            self.assertEqual(page.status_code, 200, path)
            if key:
                self.assertContains(page, f'data-page="{key}"')
            else:
                self.assertNotContains(page, "data-page=")

        session = self.client.session
        session["cart"] = {product.sku: 1}
        session.save()
        checkout = self.client.get(reverse("checkout"))
        self.assertEqual(checkout.status_code, 200)
        self.assertContains(checkout, 'data-page="checkout"')

    def test_admin_opens_one_screen_per_page(self):
        user = User.objects.create_superuser("styles", "styles@example.com", "pass-word-9")
        self.client.force_login(user)
        names = (
            "globalpagestyle",
            "homepagestyle",
            "catalogpagestyle",
            "productpagestyle",
            "cartpagestyle",
            "checkoutpagestyle",
            "aboutpagestyle",
            "legalpagestyle",
        )
        for name in names:
            row = PageStyle.objects.get(page=_page_for_admin(name))
            listing = reverse(f"admin:content_{name}_changelist")
            change = reverse(f"admin:content_{name}_change", args=[row.pk])
            self.assertRedirects(self.client.get(listing), change)
            form = self.client.get(change)
            self.assertEqual(form.status_code, 200)
            self.assertContains(form, 'type="color"', count=3)
            self.assertContains(form, "data-gestia-color")
            self.assertContains(form, "Стандарт")
            self.assertContains(form, "color_picker.js")
            model = admin.site._registry[form.context["original"].__class__]
            self.assertFalse(model.has_delete_permission(form.wsgi_request, row))
            self.assertFalse(model.has_add_permission(form.wsgi_request))
        home = self.client.get(reverse("admin:content_homepagestyle_change", args=[PageStyle.objects.get(page="home").pk]))
        self.assertContains(home, "Стандартний колір спільний")
        whole = self.client.get(
            reverse("admin:content_globalpagestyle_change", args=[PageStyle.objects.get(page="global").pk])
        )
        self.assertContains(whole, "Для всього сайту")

    def test_sidebar_lists_each_page(self):
        labels = []
        for group in build_navigation(None):
            if group["title"] != "Стилі":
                continue
            for item in group["items"]:
                labels.append(item["title"])
                for child in item.get("items") or []:
                    labels.append(child["title"])
        self.assertEqual(
            labels,
            ["Стилі", "Увесь сайт", "Головна", "Каталог", "Товар", "Кошик", "Оформлення", "Про нас", "Юридичні"],
        )


def _page_for_admin(name: str) -> str:
    return {
        "globalpagestyle": "global",
        "homepagestyle": "home",
        "catalogpagestyle": "catalog",
        "productpagestyle": "product",
        "cartpagestyle": "cart",
        "checkoutpagestyle": "checkout",
        "aboutpagestyle": "about",
        "legalpagestyle": "legal",
    }[name]
