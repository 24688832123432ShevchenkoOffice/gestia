from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from src.content.colors import TOKEN_ACCENT, TOKEN_INK, TOKEN_PAPER
from src.content.models_styles import (
    AboutPageStyle,
    CartPageStyle,
    CatalogPageStyle,
    CheckoutPageStyle,
    GlobalPageStyle,
    HomePageStyle,
    LegalPageStyle,
    PageStyle,
    ProductPageStyle,
)
from src.core.admin_base import GestiaModelAdmin
from src.core.admin_color import GestiaColorWidget

_COLOR_DEFAULTS = {
    "background_color": TOKEN_PAPER,
    "text_color": TOKEN_INK,
    "hover_color": TOKEN_ACCENT,
}
_GLOBAL_HINT = "Для всього сайту. Стандарт — як у макеті."
_PAGE_HINT = "Стандартний колір спільний для сайту."


class PageStyleAdmin(GestiaModelAdmin):
    page_key = ""
    fields = ("background_color", "text_color", "hover_color")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(page=self.page_key)

    def has_add_permission(self, request):
        if PageStyle.objects.filter(page=self.page_key).exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = PageStyle.objects.filter(page=self.page_key).first()
        if obj is None:
            obj = PageStyle.objects.create(page=self.page_key)
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)

    def save_model(self, request, obj, form, change):
        obj.page = self.page_key
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        default = _COLOR_DEFAULTS.get(db_field.name)
        if default:
            kwargs["widget"] = GestiaColorWidget(default=default)
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None and db_field.name == "background_color":
            formfield.help_text = _GLOBAL_HINT if self.page_key == PageStyle.Key.GLOBAL else _PAGE_HINT
        return formfield


def _register(model, key):
    class _Admin(PageStyleAdmin):
        page_key = key

    _Admin.__name__ = f"{model.__name__}Admin"
    admin.site.register(model, _Admin)


_register(GlobalPageStyle, PageStyle.Key.GLOBAL)
_register(HomePageStyle, PageStyle.Key.HOME)
_register(CatalogPageStyle, PageStyle.Key.CATALOG)
_register(ProductPageStyle, PageStyle.Key.PRODUCT)
_register(CartPageStyle, PageStyle.Key.CART)
_register(CheckoutPageStyle, PageStyle.Key.CHECKOUT)
_register(AboutPageStyle, PageStyle.Key.ABOUT)
_register(LegalPageStyle, PageStyle.Key.LEGAL)
