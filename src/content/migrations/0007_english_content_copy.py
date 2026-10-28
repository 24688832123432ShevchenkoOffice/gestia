from django.db import migrations

# English copy for known rows. Applied only when the Ukrainian source still matches
# and the English field is empty.

BLOCKS = {
    "hero": {
        "title": (
            "Декор для дому, текстиль \nі флористика",
            "Home decor, textiles \nand floristry",
        ),
        "text": (
            "Декор для дому, домашній текстиль, флористика та одяг для дому від Gestia Home. "
            "Створюйте затишний простір із речами, у яких поєднуються естетика та функціональність",
            "Home decor, home textiles, floristry, and clothing for the home from Gestia Home. "
            "Create a cosy space with pieces that bring aesthetics and function together.",
        ),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
    },
    "popular": {
        "title": ("Популярні товари", "Popular products"),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
    },
    "advantages": {
        "title": ("Чому обирають GESTIA HOME", "Why people choose GESTIA HOME"),
        "text": (
            "Декор для дому, флористика, текстиль та одяг для дому українського виробництва",
            "Home decor, floristry, textiles, and clothing for the home, made in Ukraine",
        ),
        "text_mobile": (
            "Декор для дому, флористика, текстиль \nта одяг для дому українського виробництва",
            "Home decor, floristry, textiles \nand clothing for the home, made in Ukraine",
        ),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
    },
    "reviews": {
        "title": ("Відгуки", "Reviews"),
    },
    "callback": {
        "title": ("Замовити зворотний дзвінок", "Request a callback"),
        "text": (
            "Залиште свій номер телефону, і ми зв’яжемося з вами найближчим часом",
            "Leave your phone number and we will contact you shortly",
        ),
        "text_mobile": (
            "Залиште свій номер телефону, \nі ми зв’яжемося з вами найближчим часом",
            "Leave your phone number, \nand we will contact you shortly",
        ),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
        "link": ("Політикою конфіденційності", "the Privacy policy"),
        "note": (
            "Погоджуюсь на обробку персональних даних згідно з ",
            "I agree to the processing of personal data according to ",
        ),
        "lines": ("Ім’я\nНомер телефону\nПовідомлення", "Name\nPhone number\nMessage"),
    },
    "locale": {
        "title": ("Країна та мова", "Country and language"),
        "text": ("Україна/Гривня ", "Ukraine/Hryvnia "),
        "cta": ("Підтвердити", "Confirm"),
        "link": ("Змінити", "Change"),
    },
    "mega": {
        "cta": ("Дивитись все", "View all"),
    },
    "catalog": {
        "cta": ("Завантажити все", "Load all"),
    },
    "pdp_ship": {
        "title": ("Доставка", "Delivery"),
        "text": (
            "Доставка «Новою поштою» по Україні — у відділення, поштомат або кур’єром\n"
            "Термін доставки — орієнтовно 1–3 робочі дні після відправлення\n"
            "Вартість доставки розраховується за тарифами перевізника\n"
            "Після відправлення ви отримаєте номер накладної для відстеження замовлення",
            "Delivery by Nova Poshta across Ukraine — to a branch, a parcel locker, or by courier\n"
            "Estimated delivery is 1–3 business days after dispatch\n"
            "The delivery cost is calculated at the carrier’s rates\n"
            "After dispatch you will receive a tracking number for the order",
        ),
    },
    "pdp_pay": {
        "title": ("Оплата", "Payment"),
        "text": (
            "Онлайн-оплата банківською карткою Visa або Mastercard\n"
            "Оплата за реквізитами банківського рахунку\n"
            "Підтвердження замовлення та деталі оплати надсилаються після оформлення",
            "Online payment by Visa or Mastercard\n"
            "Payment by bank transfer\n"
            "Order confirmation and payment details are sent after checkout",
        ),
    },
    "pdp_set": {
        "title": ("Товари з цього ж сету", "From the same set"),
        "text_mobile": ("Товари з цього сету", "From this set"),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
    },
    "pdp_related": {
        "title": ("Схожі товари", "Similar pieces"),
        "cta": ("Перейти до каталогу", "Go to the catalogue"),
    },
}

ADVANTAGES = (
    {
        "title_uk": "Унікальний дизайн",
        "title_en": "Unique design",
        "text_uk": "Декор, що поєднує сучасну естетику та природну красу",
        "text_en": "Decor that combines a contemporary look with natural beauty",
    },
    {
        "title_uk": "Українське виробництво",
        "title_en": "Made in Ukraine",
        "text_uk": "Вироби, створені в Україні \nз увагою до деталей та естетики",
        "text_en": "Pieces made in Ukraine \nwith care for detail and aesthetics",
    },
    {
        "title_uk": "Натуральні матеріали",
        "title_en": "Natural materials",
        "text_uk": "Натуральні матеріали для природної естетики та затишку вдома",
        "text_en": "Natural materials for a natural look and comfort at home",
    },
    {
        "title_uk": "Багатофункціональність",
        "title_en": "Versatility",
        "text_uk": "Речі, які легко адаптувати до різних потреб і домашніх сценаріїв",
        "text_en": "Pieces that adapt easily to different needs and ways of living at home",
    },
)

REVIEW_AUTHOR_UK = "Марія\u00a0К."
REVIEW_AUTHOR_EN = "Maria\u00a0K."
REVIEW_TEXT_UK = (
    "Дуже красивий декор, який повністю відповідає фотографіям. "
    "Усе виглядає витончено й гармонійно. Саме такі деталі створюють особливу атмосферу вдома"
)
REVIEW_TEXT_EN = (
    "Beautiful decor that matches the photographs completely. "
    "Everything looks refined and harmonious. Details like these create a special atmosphere at home."
)

FOOTER = (
    ("catalog", "", "Усі товари", "All products"),
    ("category", "rizdvyani-boksy", "Різдвяні бокси", "Christmas boxes"),
    ("category", "interierni-kompozytsii", "Інтер'єрні композиції", "Interior compositions"),
    ("category", "serviruvannia", "Сервірування", "Table setting"),
    ("about", "", "Про нас", "About"),
    ("anchor", "callback", "Контакти", "Contacts"),
    ("shipping", "", "Доставка та оплата", "Delivery and payment"),
    ("offer", "", "Публічний договір (оферта)", "Public contract (offer)"),
    ("privacy", "", "Політика конфіденційності", "Privacy policy"),
    ("cookies", "", "Політика cookies", "Cookie policy"),
)


def _fill_pair(qs, field, source, value):
    qs.filter(**{f"{field}_uk": source, f"{field}_en": ""}).update(**{f"{field}_en": value})


def _clear_pair(qs, field, source, value):
    qs.filter(**{f"{field}_uk": source, f"{field}_en": value}).update(**{f"{field}_en": ""})


def fill_english_content(apps, schema_editor):
    del schema_editor
    HomeBlock = apps.get_model("content", "HomeBlock")
    Advantage = apps.get_model("content", "Advantage")
    Review = apps.get_model("content", "Review")
    FooterLink = apps.get_model("content", "FooterLink")
    AboutPage = apps.get_model("content", "AboutPage")
    SiteSettings = apps.get_model("content", "SiteSettings")

    for key, fields in BLOCKS.items():
        block = HomeBlock.objects.filter(key=key)
        for field, (source, value) in fields.items():
            _fill_pair(block, field, source, value)
    for row in ADVANTAGES:
        found = Advantage.objects.filter(title_uk=row["title_uk"])
        found.filter(title_en="").update(title_en=row["title_en"])
        found.filter(text_uk=row["text_uk"], text_en="").update(text_en=row["text_en"])
    Review.objects.filter(author_uk=REVIEW_AUTHOR_UK, author_en="").update(author_en=REVIEW_AUTHOR_EN)
    Review.objects.filter(text_uk=REVIEW_TEXT_UK, text_en="").update(text_en=REVIEW_TEXT_EN)
    for url_name, url_arg, label_uk, label_en in FOOTER:
        FooterLink.objects.filter(
            url_name=url_name,
            url_arg=url_arg,
            label_uk=label_uk,
            label_en="",
        ).update(label_en=label_en)
    AboutPage.objects.filter(title_uk="Про нас", title_en="").update(title_en="About")
    SiteSettings.objects.filter(
        developer_note_uk="Розроблено PrometeyLabs",
        developer_note_en="",
    ).update(developer_note_en="Developed by PrometeyLabs")


def clear_english_content(apps, schema_editor):
    del schema_editor
    HomeBlock = apps.get_model("content", "HomeBlock")
    Advantage = apps.get_model("content", "Advantage")
    Review = apps.get_model("content", "Review")
    FooterLink = apps.get_model("content", "FooterLink")
    AboutPage = apps.get_model("content", "AboutPage")
    SiteSettings = apps.get_model("content", "SiteSettings")

    for key, fields in BLOCKS.items():
        block = HomeBlock.objects.filter(key=key)
        for field, (source, value) in fields.items():
            _clear_pair(block, field, source, value)
    for row in ADVANTAGES:
        found = Advantage.objects.filter(title_uk=row["title_uk"])
        found.filter(title_en=row["title_en"]).update(title_en="")
        found.filter(text_uk=row["text_uk"], text_en=row["text_en"]).update(text_en="")
    Review.objects.filter(author_uk=REVIEW_AUTHOR_UK, author_en=REVIEW_AUTHOR_EN).update(author_en="")
    Review.objects.filter(text_uk=REVIEW_TEXT_UK, text_en=REVIEW_TEXT_EN).update(text_en="")
    for url_name, url_arg, label_uk, label_en in FOOTER:
        FooterLink.objects.filter(
            url_name=url_name,
            url_arg=url_arg,
            label_uk=label_uk,
            label_en=label_en,
        ).update(label_en="")
    AboutPage.objects.filter(title_uk="Про нас", title_en="About").update(title_en="")
    SiteSettings.objects.filter(
        developer_note_uk="Розроблено PrometeyLabs",
        developer_note_en="Developed by PrometeyLabs",
    ).update(developer_note_en="")


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_remove_russian_fields"),
    ]

    operations = [
        migrations.RunPython(fill_english_content, clear_english_content),
    ]
