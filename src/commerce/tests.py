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
