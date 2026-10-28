from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from src.content.admin_limits import tighten
from src.content.models import ContactForms, HomeBlock
from src.content.proxies import (
    HomeAdvantagesBlock,
    HomeCallbackBlock,
    HomeCategoriesBlock,
    HomeHeroBlock,
    HomePopularBlock,
    HomeReviewsBlock,
    HomeVideo2Block,
    HomeVideoBlock,
)
from src.core.admin_base import GestiaModelAdmin

PHOTO_DESK = "1442×871 px. JPG або PNG."
PHOTO_MOBILE = "390×735 px. JPG або PNG."
VIDEO_HINT = "MP4 або WEBM."
CARD_PHOTO = "303×197 px. Спільне фото для всіх карток. JPG або PNG."


class KeyedBlockAdmin(GestiaModelAdmin):
    block_key = ""
    default_sort = 0
    text_limits = {}
    image_hints = {}

    def get_queryset(self, request):
        return super().get_queryset(request).filter(key=self.block_key)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = HomeBlock.objects.filter(key=self.block_key).first()
        if obj is None:
            obj = HomeBlock.objects.create(key=self.block_key, sort=self.default_sort)
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)

    def save_model(self, request, obj, form, change):
        obj.key = self.block_key
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        hint = self.image_hints.get(db_field.name, "")
        if db_field.name == "video":
            hint = VIDEO_HINT
        return tighten(formfield, self.text_limits.get(db_field.name), hint)


class HomeCallbackForm(forms.ModelForm):
    ph_name_uk = forms.CharField(label="Підказка імені", max_length=24, required=False)
    ph_name_en = forms.CharField(label="Підказка імені (EN)", max_length=24, required=False)
    ph_phone_uk = forms.CharField(label="Підказка телефону", max_length=24, required=False)
    ph_phone_en = forms.CharField(label="Підказка телефону (EN)", max_length=24, required=False)
    ph_message_uk = forms.CharField(label="Підказка повідомлення", max_length=24, required=False)
    ph_message_en = forms.CharField(label="Підказка повідомлення (EN)", max_length=24, required=False)

    class Meta:
        model = HomeCallbackBlock
        fields = (
            "title_uk",
            "title_en",
            "text_uk",
            "text_en",
            "text_mobile_uk",
            "text_mobile_en",
            "note_uk",
            "note_en",
            "link_uk",
            "link_en",
            "cta_uk",
            "cta_en",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uk = _lines(self.instance.lines_uk)
        en = _lines(self.instance.lines_en)
        self.fields["ph_name_uk"].initial = uk[0]
        self.fields["ph_phone_uk"].initial = uk[1]
        self.fields["ph_message_uk"].initial = uk[2]
        self.fields["ph_name_en"].initial = en[0]
        self.fields["ph_phone_en"].initial = en[1]
        self.fields["ph_message_en"].initial = en[2]

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.lines_uk = _join(self.cleaned_data, "uk")
        obj.lines_en = _join(self.cleaned_data, "en")
        obj.key = HomeBlock.Key.CALLBACK
        if commit:
            obj.save()
        return obj


def _lines(value):
    parts = (value or "").splitlines()
    while len(parts) < 3:
        parts.append("")
    return parts[:3]


def _join(cleaned, lang):
    return "\n".join(
        [
            cleaned.get(f"ph_name_{lang}", ""),
            cleaned.get(f"ph_phone_{lang}", ""),
            cleaned.get(f"ph_message_{lang}", ""),
        ]
    )


@admin.register(HomeHeroBlock)
class HomeHeroAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.HERO
    default_sort = 1
    text_limits = {
        "title_uk": 64,
        "title_en": 64,
        "text_uk": 200,
        "text_en": 200,
        "cta_uk": 28,
        "cta_en": 28,
    }
    image_hints = {"image": PHOTO_DESK, "image_mobile": PHOTO_MOBILE}
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "text_uk", "cta_uk")}),
        ("Англійська", {"fields": ("title_en", "text_en", "cta_en")}),
        ("Медіа", {"fields": ("image", "image_mobile", "video")}),
    )


@admin.register(HomeCategoriesBlock)
class HomeCategoriesAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.CATEGORIES
    default_sort = 2
    text_limits = {"title_uk": 20, "title_en": 20}
    fieldsets = (
        ("Назва секції", {"fields": ("title_uk", "title_en")}),
    )


@admin.register(HomeVideoBlock)
class HomeVideoAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.VIDEO
    default_sort = 3
    image_hints = {"image": PHOTO_DESK, "image_mobile": PHOTO_MOBILE}
    fieldsets = (("Медіа", {"fields": ("image", "image_mobile", "video")}),)


@admin.register(HomePopularBlock)
class HomePopularAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.POPULAR
    default_sort = 4
    text_limits = {"title_uk": 24, "title_en": 24, "cta_uk": 28, "cta_en": 28}
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "cta_uk")}),
        ("Англійська", {"fields": ("title_en", "cta_en")}),
    )


@admin.register(HomeAdvantagesBlock)
class HomeAdvantagesAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.ADVANTAGES
    default_sort = 5
    text_limits = {
        "title_uk": 36,
        "title_en": 36,
        "text_uk": 110,
        "text_en": 110,
        "text_mobile_uk": 110,
        "text_mobile_en": 110,
        "cta_uk": 28,
        "cta_en": 28,
    }
    image_hints = {"image": CARD_PHOTO}
    fieldsets = (
        ("Українська", {"fields": ("title_uk", "text_uk", "text_mobile_uk", "cta_uk")}),
        ("Англійська", {"fields": ("title_en", "text_en", "text_mobile_en", "cta_en")}),
        ("Фото", {"fields": ("image",)}),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "text_mobile_uk" and formfield is not None:
            formfield.help_text = "Для телефона. Якщо порожньо — текст із комп’ютера."
        return formfield


@admin.register(HomeVideo2Block)
class HomeVideo2Admin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.VIDEO_2
    default_sort = 6
    image_hints = {"image": PHOTO_DESK, "image_mobile": PHOTO_MOBILE}
    fieldsets = (("Медіа", {"fields": ("image", "image_mobile", "video")}),)


@admin.register(HomeReviewsBlock)
class HomeReviewsAdmin(KeyedBlockAdmin):
    block_key = HomeBlock.Key.REVIEWS
    default_sort = 7
    text_limits = {"title_uk": 16, "title_en": 16}
    fieldsets = (("Заголовок", {"fields": ("title_uk", "title_en")}),)


@admin.register(HomeCallbackBlock)
class HomeCallbackAdmin(KeyedBlockAdmin):
    form = HomeCallbackForm
    block_key = HomeBlock.Key.CALLBACK
    default_sort = 8
    text_limits = {
        "title_uk": 32,
        "title_en": 32,
        "text_uk": 100,
        "text_en": 100,
        "text_mobile_uk": 100,
        "text_mobile_en": 100,
        "note_uk": 72,
        "note_en": 72,
        "link_uk": 40,
        "link_en": 40,
        "cta_uk": 28,
        "cta_en": 28,
    }
    fieldsets = (
        ("Заголовок", {"fields": ("title_uk", "title_en")}),
        ("Підзаголовок", {"fields": ("text_uk", "text_en", "text_mobile_uk", "text_mobile_en")}),
        (
            "Підказки в полях",
            {
                "fields": (
                    "ph_name_uk",
                    "ph_name_en",
                    "ph_phone_uk",
                    "ph_phone_en",
                    "ph_message_uk",
                    "ph_message_en",
                )
            },
        ),
        ("Згода і кнопка", {"fields": ("note_uk", "note_en", "link_uk", "link_en", "cta_uk", "cta_en")}),
    )


class _SingletonAdmin(GestiaModelAdmin):
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


@admin.register(ContactForms)
class ContactFormsAdmin(_SingletonAdmin):
    fieldsets = (
        (
            "Вікно святкових боксів",
            {
                "fields": (
                    "waitlist_title_uk",
                    "waitlist_title_en",
                    "waitlist_p1_uk",
                    "waitlist_p1_en",
                    "waitlist_p2_uk",
                    "waitlist_p2_en",
                    "waitlist_p3_uk",
                    "waitlist_p3_en",
                    "waitlist_email_uk",
                    "waitlist_email_en",
                    "waitlist_consent_uk",
                    "waitlist_consent_en",
                    "waitlist_privacy_uk",
                    "waitlist_privacy_en",
                    "waitlist_button_uk",
                    "waitlist_button_en",
                    "waitlist_thanks_title_uk",
                    "waitlist_thanks_title_en",
                    "waitlist_thanks_text_uk",
                    "waitlist_thanks_text_en",
                )
            },
        ),
        (
            "Кнопки форм",
            {
                "fields": (
                    "contact_button_uk",
                    "contact_button_en",
                    "callback_button_uk",
                    "callback_button_en",
                    "buy_button_uk",
                    "buy_button_en",
                    "sheet_close_uk",
                    "sheet_close_en",
                    "sheet_consent_uk",
                    "sheet_consent_en",
                )
            },
        ),
        (
            "Підписи полів",
            {
                "fields": (
                    "label_name_uk",
                    "label_name_en",
                    "label_phone_uk",
                    "label_phone_en",
                    "label_message_uk",
                    "label_message_en",
                    "label_address_uk",
                    "label_address_en",
                    "label_email_uk",
                    "label_email_en",
                )
            },
        ),
    )
