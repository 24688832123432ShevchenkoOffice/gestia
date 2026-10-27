from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import translation

from src.catalog.models import Category, Product
from src.commerce.forms import CallbackForm
from src.commerce.models import Inquiry, Order


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

    def test_cart_add_reads_qty(self):
        response = self.client.post("/koshik/dodaty/", {"sku": "SNIH", "qty": "3"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["cart"]["SNIH"], 3)

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
        self.assertContains(checkout, "Контактні дані")
        self.assertContains(checkout, "Кур\u2019єрська доставка")
        self.assertNotContains(checkout, "Контактні данні")
        self.assertNotContains(checkout, "Курєрська доставка")
        self.assertContains(checkout, "Ваше замовлення")
        self.assertContains(checkout, "х2")
        self.assertContains(checkout, "css/pages/checkout.css")
        self.assertNotContains(checkout, "figma.com")
        html = checkout.content.decode()
        field_at = html.find('name="branch"')
        field = html[html.rfind("<input", 0, field_at):html.find(">", field_at)]
        self.assertIn('role="combobox"', field)
        self.assertIn('aria-autocomplete="list"', field)
        self.assertIn('aria-expanded="false"', field)
        self.assertIn('aria-controls="np-branch-listbox"', field)
        self.assertIn('autocomplete="off"', field)
        self.assertIn('data-np-cities-url="/zamovlennia/np/cities/"', html)
        self.assertIn('data-np-warehouses-url="/zamovlennia/np/warehouses/"', html)
        self.assertNotIn("hx-", field)
        self.assertIn(
            '<ul id="np-city-listbox" class="co-suggest__list" role="listbox" hidden>',
            html,
        )
        self.assertIn(
            '<ul id="np-branch-listbox" class="co-suggest__list" role="listbox" hidden>',
            html,
        )
        self.assertNotIn("novaposhta", html.lower())

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

    def test_np_cities_requires_two_chars(self):
        response = self.client.get("/zamovlennia/np/cities/", {"q": "к"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"], [])

    @override_settings(NOVA_POSHTA_API_KEY="", DEBUG=False)
    def test_np_cities_without_key_on_prod(self):
        response = self.client.get("/zamovlennia/np/cities/", {"q": "ки"})
        self.assertEqual(response.status_code, 503)

    @override_settings(NOVA_POSHTA_API_KEY="", DEBUG=True)
    def test_np_cities_demo_mode(self):
        response = self.client.get("/zamovlennia/np/cities/", {"q": "ки"})
        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.json()["items"]]
        self.assertTrue(any("Київ" in name for name in names))

    @override_settings(NOVA_POSHTA_API_KEY="test-key")
    @patch("src.commerce.novaposhta.search_cities")
    def test_np_cities_returns_items(self, mocked):
        mocked.return_value = [{"ref": "city-ref", "name": "м. Київ"}]
        response = self.client.get("/zamovlennia/np/cities/", {"q": "ки"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["name"], "м. Київ")
        mocked.assert_called_once_with("ки", limit=12)

    @override_settings(NOVA_POSHTA_API_KEY="test-key")
    @patch("src.commerce.novaposhta.warehouses_for_city")
    def test_np_warehouses_by_city_ref(self, mocked):
        mocked.return_value = [
            {"ref": "w1", "label": "Відділення №1: вул. Хрещатик", "number": "1"}
        ]
        response = self.client.get(
            "/zamovlennia/np/warehouses/",
            {"city_ref": "city-ref", "kind": "branch"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 1)
        mocked.assert_called_once_with("city-ref", kind="branch")

    @override_settings(NOVA_POSHTA_API_KEY="", DEBUG=True)
    def test_np_streets_demo_mode(self):
        response = self.client.get(
            "/zamovlennia/np/streets/",
            {"city_ref": "demo-kyiv", "q": "кашт"},
        )
        self.assertEqual(response.status_code, 200)
        labels = [item["label"] for item in response.json()["items"]]
        self.assertTrue(any("Каштанова" in label for label in labels))

    @override_settings(NOVA_POSHTA_API_KEY="", DEBUG=True)
    def test_np_streets_ignores_house_number(self):
        response = self.client.get(
            "/zamovlennia/np/streets/",
            {"city_ref": "demo-kyiv", "q": "вул. Каштанова 13"},
        )
        self.assertEqual(response.status_code, 200)
        labels = [item["label"] for item in response.json()["items"]]
        self.assertTrue(any("Каштанова" in label for label in labels))

    def test_checkout_courier_appends_apartment(self):
        session = self.client.session
        session["cart"] = {"SNIH": 1}
        session.save()
        response = self.client.post(
            "/zamovlennia/",
            {
                "name": "Оля",
                "phone": "+380671112233",
                "email": "olya@example.com",
                "delivery_method": "np_courier",
                "city": "Київ",
                "branch": "вул. Каштанова, 13",
                "apartment": "42",
                "payment_method": Order.Payment.ON_DELIVERY,
                "consent": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.delivery_method, "np_courier")
        self.assertEqual(order.delivery_address, "Київ, вул. Каштанова, 13, кв. 42")

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

    def test_two_products_totals_match_price_times_qty(self):
        lamp = Product.objects.create(
            category=self.product.category,
            sku="LAMP",
            slug="lampa",
            name_uk="Лампа",
            price_uah=Decimal("1500"),
            price_eur=Decimal("30"),
        )
        snow_qty, lamp_qty = 2, 3
        session = self.client.session
        session["cart"] = {"SNIH": snow_qty, "LAMP": lamp_qty}
        session["currency"] = "uah"
        session.save()
        total = self.product.price_uah * snow_qty + lamp.price_uah * lamp_qty
        self.assertEqual(total, Decimal("4700"))
        label = f"₴ {int(total):,}".replace(",", " ") + " грн"
        cart = self.client.get("/koshik/")
        checkout = self.client.get("/zamovlennia/")
        self.assertContains(cart, "Сніг")
        self.assertContains(cart, "Лампа")
        self.assertContains(cart, "100 UAH")
        self.assertContains(cart, "1 500 UAH")
        self.assertContains(cart, 'value="2"')
        self.assertContains(cart, 'value="3"')
        self.assertContains(cart, label)
        self.assertContains(checkout, "Сніг")
        self.assertContains(checkout, "Лампа")
        self.assertContains(checkout, "х2")
        self.assertContains(checkout, "х3")
        self.assertContains(checkout, label)
        self.assertNotContains(cart, "₴ 2300 грн")
        self.assertNotContains(checkout, "₴ 2300 грн")
        self.assertNotContains(cart, "2 450 UAH")
        self.assertNotContains(checkout, "2 450 UAH")

    def test_checkout_copy_translates(self):
        session = self.client.session
        session["cart"] = {"SNIH": 1}
        session.save()
        english = self.client.get("/en/zamovlennia/")
        self.assertContains(english, "Contact details")
        self.assertContains(english, "Courier delivery")
        ukrainian = self.client.get("/zamovlennia/")
        self.assertContains(ukrainian, "Контактні дані")

    def test_wishlist_session_flow(self):
        empty = self.client.get("/obrane/")
        self.assertEqual(empty.status_code, 200)
        self.assertContains(empty, "У обраному поки порожньо.")
        self.assertContains(empty, "css/pages/wishlist.css")
        added = self.client.post("/obrane/toggle/", {"sku": "SNIH"})
        self.assertEqual(added.status_code, 302)
        self.assertEqual(self.client.session["wishlist"], ["SNIH"])
        page = self.client.get("/obrane/")
        self.assertContains(page, "Сніг")
        self.assertContains(page, "Обране (1)")
        removed = self.client.post("/obrane/prybraty/", {"sku": "SNIH"})
        self.assertEqual(removed.status_code, 302)
        self.assertEqual(self.client.session.get("wishlist"), [])

    def test_thank_you_page(self):
        page = self.client.get("/thank-you/?kind=order&number=G-100")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Дякуємо за замовлення")
        self.assertContains(page, "G-100")
        self.assertContains(page, "До каталогу")
        self.assertContains(page, "css/pages/utility.css")
        legacy = self.client.get("/diakuiemo/?kind=order&number=G-100")
        self.assertEqual(legacy.status_code, 200)

    def test_checkout_redirects_to_thank_you(self):
        session = self.client.session
        session["cart"] = {"SNIH": 1}
        session.save()
        response = self.client.post(
            "/zamovlennia/",
            {
                "name": "Оля",
                "phone": "+380671112233",
                "email": "olya@example.com",
                "delivery_method": Order.Delivery.COURIER,
                "address": "Київ",
                "payment_method": Order.Payment.ON_DELIVERY,
                "consent": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/thank-you/", response["Location"])


class WaitlistTests(TestCase):
    def setUp(self):
        translation.activate("uk")

    def test_waitlist_modal_on_any_page(self):
        home = self.client.get("/")
        about = self.client.get("/pro-nas/")
        self.assertEqual(home.status_code, 200)
        self.assertEqual(about.status_code, 200)
        for page in (home, about):
            self.assertContains(page, 'id="waitlist-modal"')
            self.assertContains(page, "data-delay-ms=\"15000\"")
            self.assertContains(page, "js/pages/waitlist-modal.js")
            self.assertContains(page, "Твоє ідеальне свято вже майже у коробці")

    def test_waitlist_saves_inquiry(self):
        response = self.client.post(
            "/svyatkovi-boksy/",
            {"email": "guest@example.com", "consent": "on"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Дякуємо")
        self.assertContains(response, "data-waitlist-success")
        self.assertNotContains(response, "Не пропусти старт продажів")
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.kind, Inquiry.Kind.WAITLIST)
        self.assertEqual(inquiry.email, "guest@example.com")
        self.assertTrue(inquiry.consent)
