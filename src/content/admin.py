from django.contrib import admin
from unfold.admin import ModelAdmin

from src.content.models import AboutPage, Advantage, FooterLink, HomeBlock, PrivacyPage, Review, SiteSettings


class SingletonAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Контакти", {"fields": ("phone", "email", "instagram_url", "pinterest_url", "logo")}),
        ("Адреса", {"fields": ("address_uk", "address_ru", "address_en")}),
        ("Мови", {"fields": ("ru_enabled", "en_enabled")}),
        ("Сповіщення", {"fields": ("telegram_notify_orders", "telegram_notify_leads")}),
        ("Кольори", {"fields": ("color_ink", "color_paper", "color_accent")}),
        (
            "Підвал",
            {
                "fields": (
                    "footer_note_uk",
                    "footer_note_ru",
                    "footer_note_en",
                    "footer_tail_uk",
                    "footer_tail_ru",
                    "footer_tail_en",
                    "developer_note_uk",
                    "developer_note_ru",
                    "developer_note_en",
                )
            },
        ),
    )


@admin.register(HomeBlock)
class HomeBlockAdmin(ModelAdmin):
    list_display = ("key", "title_uk", "sort")
    list_filter = ("key",)
    search_fields = ("title_uk", "title_ru", "title_en", "text_uk")
    ordering = ("sort",)


@admin.register(Advantage)
class AdvantageAdmin(ModelAdmin):
    list_display = ("title_uk", "sort")
    search_fields = ("title_uk", "title_ru", "title_en")
    ordering = ("sort",)


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "body_uk", "seo_title_uk", "seo_description_uk")}),
        ("Російська", {"fields": ("title_ru", "body_ru", "seo_title_ru", "seo_description_ru")}),
        ("Англійська", {"fields": ("title_en", "body_en", "seo_title_en", "seo_description_en")}),
        ("Медіа", {"fields": ("image", "video")}),
    )


@admin.register(PrivacyPage)
class PrivacyPageAdmin(SingletonAdmin):
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "body_uk", "seo_title_uk", "seo_description_uk")}),
        ("Російська", {"fields": ("title_ru", "body_ru", "seo_title_ru", "seo_description_ru")}),
        ("Англійська", {"fields": ("title_en", "body_en", "seo_title_en", "seo_description_en")}),
    )


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("author_uk", "rating_kind", "sort")
    search_fields = ("author_uk", "text_uk")
    ordering = ("sort",)


@admin.register(FooterLink)
class FooterLinkAdmin(ModelAdmin):
    list_display = ("label_uk", "column", "url_name", "underlined", "sort")
    list_filter = ("column", "underlined")
    search_fields = ("label_uk", "label_ru", "label_en")
    ordering = ("column", "sort")
