from decimal import Decimal

from django.test import TestCase
from django.utils import translation

from src.catalog.models import Category, Product
from src.commerce.forms import CallbackForm
from src.commerce.models import Order


class PhoneTests(TestCase):
    def test_rejects_letters(self):
        form = CallbackForm(data={"name": "Оля", "phone": "067abc1122", "sku": "A", "consent": True})
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_accepts_digits(self):
        form = CallbackForm(data={"name": "Оля", "phone": "+380671112233", "sku": "A", "consent": True})
        self.assertTrue(form.is_valid())


class CheckoutTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        category = Category.objects.create(slug="cat", name_uk="Каталог")
        self.product = Product.objects.create(
            category=category,
            sku="SNIH",
            slug="snih",
            name_uk="Сніг",
            price_uah=Decimal("100"),
            price_eur=Decimal("2"),
        )

    def test_cart_checkout_creates_order(self):
        session = self.client.session
        session["cart"] = {"SNIH": 2}
        session["currency"] = "uah"
        session.save()
        response = self.client.post(
            "/zamovlennia/",
            {
                "name": "Оля",
                "phone": "+380671112233",
                "email": "olya@example.com",
                "delivery_method": Order.Delivery.BRANCH,
                "address": "Відділення 12",
                "payment_method": Order.Payment.ON_DELIVERY,
                "consent": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.total, Decimal("200"))
        self.assertEqual(order.items.get().qty, 2)

    def test_cart_and_checkout_pages_render(self):
        empty = self.client.get("/koshik/")
        self.assertEqual(empty.status_code, 200)
        self.assertContains(empty, "Кошик (0)")
        self.assertContains(empty, "Кошик порожній.")
        self.assertContains(empty, "css/pages/cart.css")
        session = self.client.session
        session["cart"] = {"SNIH": 2}
        session["currency"] = "uah"
        session.save()
        page = self.client.get("/koshik/")
        self.assertContains(page, "Сніг")
        self.assertContains(page, "100 UAH")
        self.assertContains(page, "₴ 200 грн")
        self.assertContains(page, "Перейти до оформлення")
        self.assertNotContains(page, "figma.com")
        checkout = self.client.get("/zamovlennia/")
        self.assertEqual(checkout.status_code, 200)
        self.assertContains(checkout, "Контактні данні")
        self.assertContains(checkout, "Курєрська доставка")
        self.assertContains(checkout, "Ваше замовлення")
        self.assertContains(checkout, "х2")
        self.assertContains(checkout, "css/pages/checkout.css")
        self.assertNotContains(checkout, "figma.com")

    def test_checkout_joins_city_and_branch(self):
        session = self.client.session
        session["cart"] = {"SNIH": 1}
        session.save()
        response = self.client.post(
            "/zamovlennia/",
            {
                "name": "Оля",
                "phone": "+380671112233",
                "email": "olya@example.com",
                "delivery_method": "np_locker",
                "city": "Київ",
                "branch": "Поштамат 5",
                "payment_method": Order.Payment.CARD,
                "consent": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.delivery_method, "np_locker")
        self.assertEqual(order.delivery_address, "Київ, Поштамат 5")
        self.assertEqual(order.payment_method, Order.Payment.CARD)

    def test_cart_update_qty(self):
        session = self.client.session
        session["cart"] = {"SNIH": 1}
        session.save()
        response = self.client.post("/koshik/kilkist/", {"sku": "SNIH", "qty": "3"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["cart"]["SNIH"], 3)
        cleared = self.client.post(
            "/koshik/kilkist/",
            {"sku": "SNIH", "qty": "0"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(cleared.status_code, 200)
        self.assertContains(cleared, "Кошик порожній.")
        self.assertNotIn("SNIH", self.client.session.get("cart", {}))
