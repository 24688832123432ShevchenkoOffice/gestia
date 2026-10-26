# CONTENT_MANIFEST — Gestia

mode: typed singletons + фіксовані блоки. Не SiteBlock, не конструктор сторінок.
seed command: `python manage.py seed_demo`
CMS_ALLOW_STATIC_FALLBACK=false
мова контенту: *_uk / *_ru / *_en, fallback на uk якщо переклад порожній.
UI-рядки: gettext, не поля моделей.

| surface | mode | model | key / field | kind | required |
|---|---|---|---|---|---|
| header | typed | SiteSettings | phone, email, address_*, logo | text/image | phone |
| header | tokens | SiteSettings | color_ink, color_paper, color_accent | color | yes |
| footer | typed | SiteSettings | footer_note_* | text | no |
| home hero | typed | HomeBlock | key=hero title_*, text_*, image, video | text/image/video | title_uk, image |
| home categories intro | typed | HomeBlock | key=categories title_*, text_*, video | text/video | title_uk |
| home advantages intro | typed | HomeBlock | key=advantages title_*, text_*, video | text/video | title_uk |
| home advantage row | typed | Advantage | title_*, text_* | text | 3 rows |
| about | typed | AboutPage | title_*, body_*, image, video, seo_* | text/image/video | title_uk, body_uk |
| privacy | typed | PrivacyPage | title_*, body_*, seo_* | text | title_uk, body_uk |
| theme.css | tokens | SiteSettings | colors | css vars | yes |

Категорії, товари, ціни, замовлення, заявки — див. docs/tables.md, не цей маніфест.

Виняток allowlist: кредит PrometeyLabs лише на головній, rel=nofollow.
