from django.contrib import admin

from src.content.admin_limits import tighten
from src.content.models import AboutPage, Advantage, FooterLink, HomeBlock, PrivacyPage, Review, SiteSettings
from src.core.admin_base import GestiaModelAdmin

# Реєстрація окремих блоків головної і форм.
import src.content.admin_blocks  # noqa: F401, E402


class SingletonAdmin(GestiaModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Контакти", {"fields": ("phone", "email", "instagram_url", "pinterest_url", "logo")}),
        ("Адреса", {"fields": ("address_uk", "address_en")}),
        ("Мови", {"fields": ("en_enabled",)}),
        ("Сповіщення", {"fields": ("telegram_notify_orders", "telegram_notify_leads")}),
        ("Кольори", {"fields": ("color_ink", "color_paper", "color_accent")}),
        (
            "Підвал",
            {
                "fields": (
                    "footer_note_uk",
                    "footer_note_en",
                    "developer_note_uk",
                    "developer_note_en",
                )
            },
        ),
    )


@admin.register(HomeBlock)
class HomeBlockAdmin(GestiaModelAdmin):
    list_display = ("key", "title_uk", "sort")
    list_filter = ("key",)
    search_fields = ("title_uk", "title_en", "text_uk")
    ordering = ("sort",)


@admin.register(Advantage)
class AdvantageAdmin(GestiaModelAdmin):
    list_display = ("title_uk", "sort")
    search_fields = ("title_uk", "title_en")
    ordering = ("sort",)
    text_limits = {"title_uk": 24, "title_en": 24, "text_uk": 80, "text_en": 80}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        hint = ""
        if db_field.name == "image":
            hint = "303×197 px. Якщо порожньо — лишається фото блоку «Переваги». JPG або PNG."
        return tighten(formfield, self.text_limits.get(db_field.name), hint)


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "body_uk", "seo_title_uk", "seo_description_uk")}),
        ("Англійська", {"fields": ("title_en", "body_en", "seo_title_en", "seo_description_en")}),
        ("Медіа", {"fields": ("image", "video")}),
    )


@admin.register(PrivacyPage)
class PrivacyPageAdmin(SingletonAdmin):
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "body_uk", "seo_title_uk", "seo_description_uk")}),
        ("Англійська", {"fields": ("title_en", "body_en", "seo_title_en", "seo_description_en")}),
    )


@admin.register(Review)
class ReviewAdmin(GestiaModelAdmin):
    list_display = ("author_uk", "rating_kind", "sort")
    search_fields = ("author_uk", "text_uk")
    ordering = ("sort",)
    text_limits = {"author_uk": 24, "author_en": 24, "text_uk": 180, "text_en": 180}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return tighten(formfield, self.text_limits.get(db_field.name))


@admin.register(FooterLink)
class FooterLinkAdmin(GestiaModelAdmin):
    list_display = ("label_uk", "column", "url_name", "underlined", "sort")
    list_filter = ("column", "underlined")
    search_fields = ("label_uk", "label_en")
    ordering = ("column", "sort")
