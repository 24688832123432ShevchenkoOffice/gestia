# tables.md — Gestia

APPS_VARIANT=B-admin
FACET_STACK=A
PRICING=admin_dual_currency
LANGUAGES=uk,en
FALLBACK=uk

Немає apps: pricing, shipping, seo, integrations, authentication.
Немає TTN, націнки, ERP. Доставка — snapshot на Order.
Оплата карткою фіксується як спосіб; еквайринг підключається окремо, коли будуть ключі.

## CMS slots | DB regions

| Сторінка | CMS (content) | DB |
|---|---|---|
| Головна | HomeBlock hero/categories/advantages, Advantage, SiteSettings | Category (рейка) |
| Про нас | AboutPage | — |
| Політика | PrivacyPage | — |
| Каталог / категорія | порожній стан — UI gettext | Category, Product, ProductAttribute |
| Картка | — | Product, images, set, related |
| Кошик / оформлення | — | session cart, Order |
| Заявки | — | Inquiry |

Product, Category, Order, Attribute не входять у CONTENT_MANIFEST.

## Таблиці

### content_sitesettings (pk=1)
phone, email, address_uk/en, instagram_url, logo,
en_enabled, telegram_notify_orders, telegram_notify_leads,
color_ink, color_paper, color_accent, footer_note_uk/en

### content_homeblock
key unique: hero | categories | advantages
title_*, text_*, image, video, sort

### content_advantage
title_*, text_*, sort

### content_aboutpage / content_privacypage (pk=1)
title_*, body_*, image, video (about), seo_title_*, seo_description_*

### catalog_category
parent_id nullable, slug unique, name_*, image, is_active, sort
index (is_active, sort)

### catalog_productattributegroup
slug unique ∈ {style, color}, name_*

### catalog_productattribute
group_id, slug, name_*, is_filterable, show_on_pdp
unique (group_id, slug)

### catalog_product
category_id, product_set_id nullable, sku unique, slug unique,
name_*, description_*, price_uah, price_eur,
stock_status ∈ {in_stock, on_order, out},
is_active, sort, seo_title_*, seo_description_*
M2M filter_attrs, related_manual
index (is_active, category_id)
index (sku)

Пошук `q`: icontains по name_* + iexact sku.
План індексу: до 2000 SKU вистачає btree. Після цього — окрема postgres-міграція `pg_trgm` + GinIndex на name_uk/name_en. На SQLite GIN не створюється.

### catalog_productimage
product_id, image, sort

### catalog_productset
slug unique, name_*

### commerce_order
number unique, source ∈ {cart, buy_now},
customer_name, phone, email, language, currency,
delivery_method ∈ {np_branch, np_courier}, delivery_address,
payment_method ∈ {card, on_delivery}, payment_status ∈ {unpaid, awaiting, paid},
total, consent, created_at

### commerce_orderitem
order_id, sku, name, qty, unit_price, currency

### commerce_inquiry
kind ∈ {callback, contact}, name, phone, email, message,
product_id nullable, product_name, sku, consent, created_at

## URL фасетів

`/katalog/?style=scandi&color=white&q=плед`
OR усередині групи, AND між групами. `q` зберігається при скиданні фасетів.

## Меню

Джерело категорій у шапці — `Category` queryset (активні, з товарами або з такими дітьми). Окремого меню в CMS немає.

## Seed

`python manage.py load_figma_content` — контент головної з макета Figma.
