import shutil
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from src.catalog.models import (
    Category,
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductImage,
    ProductSet,
)
from src.content.models import (
    AboutPage,
    Advantage,
    FooterLink,
    HomeBlock,
    Review,
    SiteSettings,
)

DESKTOP = Path(settings.BASE_DIR) / "docs" / "figma" / "desktop"
MOBILE = Path(settings.BASE_DIR) / "docs" / "figma" / "mobile"
ZERO = Decimal("0.00")
CTA = "Перейти до каталогу"


def nb(text):
    return text.replace(" ", "\u00a0")


REVIEW = (
    "Дуже красивий декор, який повністю відповідає фотографіям. "
    "Усе виглядає витончено й гармонійно. Саме такі деталі створюють особливу атмосферу вдома"
)


def _save(instance, field, path, name=None):
    current = getattr(instance, field)
    if getattr(current, "name", ""):
        current.delete(save=False)
    with path.open("rb") as handle:
        current.save(name or path.name, File(handle), save=True)


class Command(BaseCommand):
    help = "Завантажує тексти, ціни й зображення головної з docs/figma."

    def handle(self, *args, **options):
        self._wipe()
        categories = self._categories()
        self._products(categories)
        self._blocks()
        self._advantages()
        self._reviews()
        self._footer()
        self._settings()
        self._clear_demo_pages()
        seed = Path(settings.MEDIA_ROOT) / "seed"
        if seed.exists():
            shutil.rmtree(seed)
        self.stdout.write(self.style.SUCCESS("load_figma_content завершено"))

    def _wipe(self):
        for image in ProductImage.objects.all():
            image.image.delete(save=False)
        Product.objects.all().delete()
        for category in Category.objects.all():
            if category.image:
                category.image.delete(save=False)
        Category.objects.all().delete()
        ProductSet.objects.all().delete()
        ProductAttribute.objects.all().delete()
        ProductAttributeGroup.objects.all().delete()
        Advantage.objects.all().delete()
        Review.objects.all().delete()
        FooterLink.objects.all().delete()
        for block in HomeBlock.objects.all():
            if block.image:
                block.image.delete(save=False)
            if block.image_mobile:
                block.image_mobile.delete(save=False)
        HomeBlock.objects.all().delete()

    def _categories(self):
        specs = (
            ("rizdvyani-boksy", "Різдвяні бокси", "db3d5.png", 1, 1, True),
            ("interierni-kompozytsii", "Інтерєрні композиції", "dd136.png", 2, 2, False),
            ("serviruvannia", "Сервірування", "fed6d.png", 3, 3, False),
            ("novorichnyi-dekor", "Новорічний декор", "", 4, None, False),
            ("vazy-ta-kashpo", "Вази та кашпо", "6fbc8.png", 5, 4, False),
            ("tekstyl", "Текстиль ", "", 6, None, False),
            ("svichky", "Свічки", "328df.png", 7, 6, False),
            ("podarunkovi-sety", "Подарункові сети", "14fec.png", 8, 5, False),
        )
        made = {}
        for slug, name, image, sort, home_sort, featured in specs:
            category = Category.objects.create(
                slug=slug,
                name_uk=name,
                sort=sort,
                home_sort=home_sort,
                menu_featured=featured,
                is_active=True,
            )
            if image:
                _save(category, "image", DESKTOP / image)
            made[slug] = category
        return made

    def _products(self, categories):
        specs = (
            ("GH-01", "velykodnii-ukrainskyi", "Бокс Великодній «Украіньсикй»", "479da.png", "8990.00", 400, 1, "podarunkovi-sety"),
            ("GH-02", "boks-rizdvyanyi-shyshky", "Бокс «Різдвяний Шишки»", "db3d5.png", "4980.00", 400, 2, "rizdvyani-boksy"),
            ("GH-03", "velykodnii-hnizdo", "Бокс Великодній «Гніздо»", "14fec.png", "2450.00", 400, 3, "podarunkovi-sety"),
            ("GH-04", "vesilnyi", "Бокс «Весільний»", "72b4d.png", "14980.00", 500, 4, "podarunkovi-sety"),
        )
        for sku, slug, name, image, price, weight, sort, category_slug in specs:
            product = Product.objects.create(
                category=categories[category_slug],
                sku=sku,
                slug=slug,
                name_uk=name,
                menu_name_uk="Бокс Різдвяний Шишки" if slug == "boks-rizdvyanyi-shyshky" else "",
                price_uah=Decimal(price),
                price_eur=ZERO,
                price_weight=weight,
                is_popular=True,
                is_active=True,
                sort=sort,
            )
            shot = ProductImage(product=product, sort=1)
            _save(shot, "image", DESKTOP / image, f"{slug}.png")

    def _blocks(self):
        hero_title = "Декор для дому, текстиль \nі флористика"
        hero_text = (
            "Декор для дому, домашній текстиль, флористика та одяг для дому від Gestia Home. "
            "Створюйте затишний простір із речами, у яких поєднуються естетика та функціональність"
        )
        advantage_text = (
            "Декор для дому, флористика, текстиль та одяг для дому українського виробництва"
        )
        advantage_mobile = (
            "Декор для дому, флористика, текстиль \nта одяг для дому українського виробнитва"
        )
        callback_text = "Залиште свій номер телефону, і ми зв’яжемося з вами найближчим часом"
        callback_mobile = (
            "Залиште свій номер телефону, \nі ми зв’яжемося з вами найближчим часом"
        )
        rows = (
            ("hero", 1, hero_title, hero_text, "", CTA, "", "", "1b95b.png", "0c378.png"),
            ("video", 2, "", "", "", "", "", "", "1b95b.png", "0c378.png"),
            ("popular", 3, "Популярні товари", "", "", CTA, "", "", "", ""),
            (
                "advantages",
                4,
                "Чому обирають GESTIA HOME",
                advantage_text,
                advantage_mobile,
                CTA,
                "",
                "",
                "656fe.png",
                "",
            ),
            ("video_2", 5, "", "", "", "", "", "", "1b95b.png", "0c378.png"),
            ("reviews", 6, "Відгуки", "", "", "", "", "", "", ""),
            (
                "callback",
                7,
                "Замовити зворотний дзвінок",
                callback_text,
                callback_mobile,
                CTA,
                "Політикою конфіденційності",
                "Погоджуюсь на обробку персональних даних згідно з ",
                "",
                "",
            ),
            ("locale", 8, "Країна та мова", "Україна/Гривня ", "", "Підтвердити", "Змінити", "", "", ""),
            ("mega", 9, "", "", "", "Дивитись все", "", "", "", ""),
        )
        for key, sort, title, text, mobile_text, cta, link, note, image, mobile in rows:
            block = HomeBlock.objects.create(
                key=key,
                sort=sort,
                title_uk=title,
                text_uk=text,
                text_mobile_uk=mobile_text,
                cta_uk=cta,
                link_uk=link,
                note_uk=note,
                lines_uk="Ім’я\nНомер телефону\nПовідомлення" if key == "callback" else "",
            )
            if image:
                _save(block, "image", DESKTOP / image, f"{key}-{image}")
            if mobile:
                _save(block, "image_mobile", MOBILE / mobile, f"{key}-{mobile}")

    def _advantages(self):
        rows = (
            ("Унікальний дизайн", "Декор, що поєднує сучасну естетику та природну красу"),
            (
                "Українське виробництво",
                "Вироби, створені в Україні \nз увагою до деталей та естетики",
            ),
            ("Натуральні матеріали", "Натуральні матеріали для природної естетики та затишку вдома"),
            (
                "Багатофункціональність",
                "Речі, які легко адаптувати до різних потреб і домашніх сценаріїв",
            ),
        )
        for sort, (title, text) in enumerate(rows, start=1):
            Advantage.objects.create(sort=sort, title_uk=title, text_uk=text)

    def _reviews(self):
        for sort in range(1, 5):
            Review.objects.create(
                sort=sort,
                author_uk=nb("Марія К."),
                text_uk=REVIEW,
                rating_kind=Review.Rating.BLACK_FIVE if sort == 4 else Review.Rating.GOLD_FOUR,
            )

    def _footer(self):
        rows = (
            ("category", "Усі товари", "catalog", "", False, 1),
            ("category", "Різдвяні бокси", "category", "rizdvyani-boksy", True, 2),
            ("category", "Інтерєрні композиції", "category", "interierni-kompozytsii", False, 3),
            ("category", "Сервірування", "category", "serviruvannia", False, 4),
            ("info", "Про нас", "about", "", False, 1),
            ("info", "Контакти", "anchor", "callback", False, 2),
            ("info", "Доставка та оплата", "", "", False, 3),
            ("legal", "Публічний договір (офферта)", "", "", False, 1),
            ("legal", "Політика конфедиційності", "privacy", "", False, 2),
            ("legal", "Політика cookies", "", "", False, 3),
        )
        for column, label, url_name, url_arg, underlined, sort in rows:
            FooterLink.objects.create(
                column=column,
                label_uk=label,
                url_name=url_name,
                url_arg=url_arg,
                underlined=underlined,
                sort=sort,
            )

    def _settings(self):
        site = SiteSettings.load()
        site.phone = "+380 000 00 00"
        site.instagram_url = ""
        site.pinterest_url = ""
        site.footer_note_uk = "© Gestia Home 2026. У|сі права захищені."
        site.developer_note_uk = "Розроблено PrometeyLabs"
        site.save()

    def _clear_demo_pages(self):
        about = AboutPage.objects.filter(pk=1, title_uk="Про майстерню").first()
        if about is None:
            return
        if about.image:
            about.image.delete(save=False)
        about.title_uk = "Про нас"
        about.title_ru = ""
        about.title_en = ""
        about.body_uk = ""
        about.body_ru = ""
        about.body_en = ""
        about.save()
