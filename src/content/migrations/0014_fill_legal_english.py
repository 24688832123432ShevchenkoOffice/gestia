from django.db import migrations


def _english_values():
    from src.content.legal_copy import sections_to_html
    from src.content.legal_copy_en import DOCS_EN

    values = {}
    for key, factory in DOCS_EN.items():
        doc = factory()
        values[key] = {
            "title_en": doc["title"],
            "body_en": sections_to_html(doc["sections"]),
            "seo_title_en": doc["seo_title"],
            "seo_description_en": doc["seo_description"],
        }
    return values


def fill_empty_legal_english(apps, schema_editor):
    del schema_editor
    LegalPage = apps.get_model("content", "LegalPage")
    for key, fields in _english_values().items():
        page = LegalPage.objects.filter(key=key).first()
        if page is None:
            continue
        updates = {}
        for name, value in fields.items():
            if not (getattr(page, name) or "").strip():
                updates[name] = value
        if updates:
            LegalPage.objects.filter(pk=page.pk).update(**updates)


def clear_filled_legal_english(apps, schema_editor):
    del schema_editor
    LegalPage = apps.get_model("content", "LegalPage")
    for key, fields in _english_values().items():
        page = LegalPage.objects.filter(key=key).first()
        if page is None:
            continue
        updates = {}
        for name, value in fields.items():
            if getattr(page, name) == value:
                updates[name] = ""
        if updates:
            LegalPage.objects.filter(pk=page.pk).update(**updates)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_page_styles"),
    ]

    operations = [
        migrations.RunPython(fill_empty_legal_english, clear_filled_legal_english),
    ]
