from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from tinymce.widgets import TinyMCE

from src.content.admin_limits import tighten
from src.content.models import AboutPage
from src.content.models_about import AboutGalleryItem, AboutPick
from src.content.proxies import FooterChrome
from src.core.admin_base import GestiaModelAdmin, GestiaTabularInline


class _OpenSingleton(GestiaModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)


class AboutGalleryInline(GestiaTabularInline):
    model = AboutGalleryItem
    extra = 0
    max_num = 3
    fields = ("slot", "sort", "media_kind", "image", "image_mobile", "video", "poster")


class AboutPickInline(GestiaTabularInline):
    model = AboutPick
    extra = 0
    max_num = 2
    fields = ("sort", "title_uk", "title_en", "price", "slug", "modifier", "image")


@admin.register(AboutPage)
class AboutPageAdmin(_OpenSingleton):
    inlines = (AboutGalleryInline, AboutPickInline)
    text_limits = {"title_uk": 24, "title_en": 24}
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "lead_uk", "body_uk")}),
        ("Англійська", {"fields": ("title_en", "lead_en", "body_en")}),
        ("Банер", {"fields": ("media_kind", "image", "image_mobile", "video", "poster")}),
        (
            "Пошук",
            {"fields": ("seo_title_uk", "seo_title_en", "seo_description_uk", "seo_description_en")},
        ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in {"body_uk", "body_en"}:
            kwargs["widget"] = TinyMCE(mce_attrs=settings.TINYMCE_DEFAULT_CONFIG)
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return tighten(formfield, self.text_limits.get(db_field.name))


@admin.register(FooterChrome)
class FooterChromeAdmin(_OpenSingleton):
    fieldsets = (
        ("Підпис унизу", {"fields": ("footer_note_uk", "footer_note_en")}),
        ("Рядок PrometeyLabs", {"fields": ("credit_uk", "credit_en")}),
        ("Службовий підпис", {"fields": ("developer_note_uk", "developer_note_en")}),
    )
