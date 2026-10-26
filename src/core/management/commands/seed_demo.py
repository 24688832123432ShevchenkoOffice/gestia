from decimal import Decimal
from pathlib import Path

from decouple import config

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from src.catalog.models import (
    Category,
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductSet,
)
from src.content.models import AboutPage, Advantage, HomeBlock, PrivacyPage, SiteSettings

SWATCHES = Path("media") / "seed"


def paint(name, base, band):
    SWATCHES.mkdir(parents=True, exist_ok=True)
    path = SWATCHES / name
    image = Image.new("RGB", (900, 1120), base)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 780, 900, 1120), fill=band)
    draw.rectangle((70, 120, 180, 980), fill=band)
    image.save(path, "JPEG", quality=86)
    return path


def attach(instance, field, path):
    current = getattr(instance, field)
    if current:
        return
    with path.open("rb") as handle:
        current.save(path.name, File(handle), save=True)


class Command(BaseCommand):
    help = "Ідемпотентний демо-каталог і тексти сайту."

    def handle(self, *args, **options):
        self._settings()
        self._pages()
        categories = self._categories()
        groups = self._attrs()
        sets = self._sets()
        self._products(categories, groups, sets)
        self._admin()
        self.stdout.write(self.style.SUCCESS("seed_demo завершено"))

    def _settings(self):
        site, _created = SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "phone": "+380441112233",
                "email": "studio@gestia.local",
                "address_uk": "Київ, майстерня Gestia",
                "address_ru": "Киев, мастерская Gestia",
                "address_en": "Kyiv, Gestia studio",
                "footer_note_uk": "Інтер'єрні композиції та сети",
                "footer_note_ru": "Интерьерные композиции и сеты",
                "footer_note_en": "Interior compositions and sets",
                "ru_enabled": True,
                "en_enabled": True,
            },
        )
        site.save()

    def _pages(self):
        hero_img = paint("hero.jpg", (232, 220, 204), (141, 59, 42))
        blocks = [
            ("hero", 1, "Композиції, які тримають кімнату", "Сети для столу, полиці й вікна. Ціна в гривні або в євро — перемикається вгорі.", "Композиции, которые держат комнату", "Сеты для стола, полки и окна.", "Compositions that hold a room", "Sets for the table, shelf and window."),
            ("categories", 2, "Розділи", "Оберіть напрям — далі фільтр за стилем і кольором.", "Разделы", "Дальше фильтр по стилю и цвету.", "Sections", "Then filter by style and colour."),
            ("advantages", 3, "Як ми працюємо", "", "Как мы работаем", "", "How the studio works", ""),
        ]
        for key, sort, uk, text_uk, ru, text_ru, en, text_en in blocks:
            block, _created = HomeBlock.objects.update_or_create(
                key=key,
                defaults={
                    "sort": sort,
                    "title_uk": uk,
                    "title_ru": ru,
                    "title_en": en,
                    "text_uk": text_uk,
                    "text_ru": text_ru,
                    "text_en": text_en,
                },
            )
            if key == "hero":
                attach(block, "image", hero_img)
        advantages = [
            ("01", "Збірка сету в майстерні", "Склад сету задаєте ви: ваза, свічки, текстиль.", "Сборка сета в мастерской", "Состав сета задаёте вы.", "Assembled in the studio", "You decide what belongs in the set."),
            ("02", "Дві валюти без перерахунку «на око»", "Гривня і євро зберігаються окремо.", "Две валюты", "Гривна и евро хранятся отдельно.", "Two currencies", "Hryvnia and euro are stored separately."),
            ("03", "Заявка або кошик", "Можна залишити телефон або оформити доставку.", "Заявка или корзина", "Можно оставить телефон или оформить доставку.", "A call or a basket", "Leave a phone number or place the delivery."),
        ]
        for index, (_num, uk, text_uk, ru, text_ru, en, text_en) in enumerate(advantages, start=1):
            Advantage.objects.update_or_create(
                title_uk=uk,
                defaults={
                    "sort": index,
                    "title_ru": ru,
                    "title_en": en,
                    "text_uk": text_uk,
                    "text_ru": text_ru,
                    "text_en": text_en,
                },
            )
        about, _created = AboutPage.objects.update_or_create(
            pk=1,
            defaults={
                "title_uk": "Про майстерню",
                "title_ru": "О мастерской",
                "title_en": "The studio",
                "body_uk": "Gestia збирає інтер'єрні сети: сезонні композиції, текстиль і предмети, які живуть разом, а не поодинці.\n\nФото й відео блоків змінюються в адмінці.",
                "body_ru": "Gestia собирает интерьерные сеты: сезонные композиции, текстиль и предметы, которые живут вместе.",
                "body_en": "Gestia assembles interior sets: seasonal compositions, textiles and objects meant to live together.",
            },
        )
        attach(about, "image", paint("about.jpg", (90, 74, 62), (232, 220, 204)))
        PrivacyPage.objects.update_or_create(
            pk=1,
            defaults={
                "title_uk": "Політика конфіденційності",
                "title_ru": "Политика конфиденциальности",
                "title_en": "Privacy policy",
                "body_uk": "Ім'я, телефон, email і адреса доставки потрібні, щоб зібрати замовлення і передзвонити. Дані не передаються для чужої реклами. Заявку можна відкликати листом на адресу майстерні.",
                "body_ru": "Имя, телефон, email и адрес доставки нужны, чтобы собрать заказ и перезвонить.",
                "body_en": "Name, phone, email and delivery address are used to fulfil the order and call you back.",
            },
        )

    def _categories(self):
        specs = [
            ("interier", None, "Інтер'єрні композиції", "Интерьерные композиции", "Interior compositions", (196, 168, 142), (90, 74, 62)),
            ("newyear", None, "Новорічні сети", "Новогодние сеты", "New Year sets", (47, 93, 69), (232, 220, 204)),
            ("textile", None, "Текстиль", "Текстиль", "Textiles", (141, 59, 42), (243, 238, 230)),
        ]
        made = {}
        for slug, _parent, uk, ru, en, base, band in specs:
            cat, _created = Category.objects.update_or_create(
                slug=slug,
                defaults={"name_uk": uk, "name_ru": ru, "name_en": en, "is_active": True, "parent": None},
            )
            attach(cat, "image", paint(f"cat-{slug}.jpg", base, band))
            made[slug] = cat
        child, _created = Category.objects.update_or_create(
            slug="pledy",
            defaults={
                "name_uk": "Пледи",
                "name_ru": "Пледы",
                "name_en": "Throws",
                "parent": made["textile"],
                "is_active": True,
            },
        )
        attach(child, "image", paint("cat-pledy.jpg", (232, 220, 204), (141, 59, 42)))
        made["pledy"] = child
        return made

    def _attrs(self):
        style, _created = ProductAttributeGroup.objects.update_or_create(
            slug=ProductAttributeGroup.Slug.STYLE,
            defaults={"name_uk": "Стиль", "name_ru": "Стиль", "name_en": "Style"},
        )
        color, _created = ProductAttributeGroup.objects.update_or_create(
            slug=ProductAttributeGroup.Slug.COLOR,
            defaults={"name_uk": "Колір", "name_ru": "Цвет", "name_en": "Colour"},
        )
        values = {}
        for group, slug, uk, ru, en in (
            (style, "scandi", "Скандинавський", "Скандинавский", "Scandi"),
            (style, "classic", "Класичний", "Классический", "Classic"),
            (color, "white", "Білий", "Белый", "White"),
            (color, "green", "Зелений", "Зелёный", "Green"),
            (color, "bordeaux", "Бордо", "Бордо", "Bordeaux"),
        ):
            attr, _created = ProductAttribute.objects.update_or_create(
                group=group,
                slug=slug,
                defaults={"name_uk": uk, "name_ru": ru, "name_en": en, "is_filterable": True, "show_on_pdp": True},
            )
            values[slug] = attr
        return values

    def _sets(self):
        made = {}
        for slug, uk, ru, en in (
            ("rizdvo", "Різдвяний сет", "Рождественский сет", "Christmas set"),
            ("kreda", "Сет «Крейда»", "Сет «Мел»", "Chalk set"),
        ):
            made[slug], _created = ProductSet.objects.update_or_create(
                slug=slug,
                defaults={"name_uk": uk, "name_ru": ru, "name_en": en},
            )
        return made

    def _products(self, categories, groups, sets):
        rows = [
            ("SNIH", "snih", categories["newyear"], sets["rizdvo"], "Композиція «Сніг»", "Композиция «Снег»", "Snow composition", "Ялинові гілки, біла кераміка, лляна стрічка.", "1200.00", "28.00", ["scandi", "white"], "in_stock"),
            ("HVOYA", "hvoya", categories["newyear"], sets["rizdvo"], "Вінок «Хвоя»", "Венок «Хвоя»", "Pine wreath", "Жива хвоя в класичній в'язці.", "980.00", "23.00", ["classic", "green"], "in_stock"),
            ("KREIDA", "kreida", categories["interier"], sets["kreda"], "Ваза «Крейда»", "Ваза «Мел»", "Chalk vase", "Матова ваза для сухоцвіту.", "760.00", "18.00", ["scandi", "white"], "in_stock"),
            ("BORDO", "bordo", categories["interier"], sets["kreda"], "Композиція «Бордо»", "Композиция «Бордо»", "Bordeaux composition", "Сухоцвіт і скло бордового тону.", "1450.00", "34.00", ["classic", "bordeaux"], "on_order"),
            ("OVES", "oves", categories["pledy"], None, "Плед «Овес»", "Плед «Овёс»", "Oat throw", "Вовна, світлий уток.", "2100.00", "49.00", ["scandi", "white"], "in_stock"),
            ("VINO", "vyno", categories["pledy"], None, "Плед «Вино»", "Плед «Вино»", "Wine throw", "Щільний плед бордового відтінку.", "2300.00", "54.00", ["classic", "bordeaux"], "out"),
        ]
        products = []
        for sku, slug, category, product_set, uk, ru, en, text, uah, eur, attr_slugs, stock in rows:
            product, _created = Product.objects.update_or_create(
                sku=sku,
                defaults={
                    "slug": slug,
                    "category": category,
                    "product_set": product_set,
                    "name_uk": uk,
                    "name_ru": ru,
                    "name_en": en,
                    "description_uk": text,
                    "description_ru": text,
                    "description_en": text,
                    "price_uah": Decimal(uah),
                    "price_eur": Decimal(eur),
                    "stock_status": stock,
                    "is_active": True,
                },
            )
            product.filter_attrs.set([groups[slug_name] for slug_name in attr_slugs])
            if not product.images.exists():
                path = paint(f"{sku.lower()}.jpg", (232, 220, 204), (90, 74, 62))
                with path.open("rb") as handle:
                    product.images.create(image=File(handle, name=path.name), sort=0)
            products.append(product)
        products[0].related_manual.set([products[1]])

    def _admin(self):
        password = config("SEED_ADMIN_PASSWORD", default="")
        if not password:
            return
        User = get_user_model()
        if User.objects.filter(username="admin").exists():
            return
        User.objects.create_superuser("admin", "admin@gestia.local", password)
