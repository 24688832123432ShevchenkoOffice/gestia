from django.db import migrations, models


def seed_nav_labels(apps, schema_editor):
    del schema_editor
    from src.content.literals import LITERALS

    AboutPage = apps.get_model("content", "AboutPage")
    SiteSettings = apps.get_model("content", "SiteSettings")
    page = AboutPage.objects.filter(pk=1).first()
    if page is not None:
        updates = {}
        for key in ("crumb", "story_label"):
            uk, en = LITERALS[key]
            if not getattr(page, f"{key}_uk"):
                updates[f"{key}_uk"] = uk
            if not getattr(page, f"{key}_en"):
                updates[f"{key}_en"] = en
        if updates:
            AboutPage.objects.filter(pk=page.pk).update(**updates)
    settings_row = SiteSettings.objects.filter(pk=1).first()
    if settings_row is None:
        return
    uk, en = LITERALS["menu_title"]
    chrome = {}
    if not settings_row.menu_title_uk:
        chrome["menu_title_uk"] = uk
    if not settings_row.menu_title_en:
        chrome["menu_title_en"] = en
    if chrome:
        SiteSettings.objects.filter(pk=settings_row.pk).update(**chrome)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0009_about_header_footer"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutpage",
            name="crumb_en",
            field=models.CharField(blank=True, max_length=16, verbose_name="Посилання «Головна» (EN)"),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="crumb_uk",
            field=models.CharField(blank=True, max_length=16, verbose_name="Посилання «Головна»"),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="story_label_en",
            field=models.CharField(blank=True, max_length=32, verbose_name="Назва історії (EN)"),
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="story_label_uk",
            field=models.CharField(blank=True, max_length=32, verbose_name="Назва історії"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="menu_title_en",
            field=models.CharField(blank=True, max_length=16, verbose_name="Заголовок у меню (EN)"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="menu_title_uk",
            field=models.CharField(
                blank=True,
                help_text="У мобільному меню. Кнопка в шапці лишається своєю.",
                max_length=16,
                verbose_name="Заголовок у меню",
            ),
        ),
        migrations.RunPython(seed_nav_labels, migrations.RunPython.noop),
    ]
