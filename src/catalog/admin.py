from django.contrib import admin

from src.catalog.models import (
    CatalogCell,
    Category,
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductImage,
    ProductSet,
)
from src.core.admin_base import GestiaModelAdmin, GestiaTabularInline
from src.core.admin_slug import SlugAdminMixin


class ProductImageInline(GestiaTabularInline):
    model = ProductImage
    fields = ("image", "sort", "frame_height", "frame_top")
    extra = 1


@admin.register(Category)
class CategoryAdmin(SlugAdminMixin, GestiaModelAdmin):
    list_display = (
        "name_uk",
        "parent",
        "slug",
        "is_active",
        "sort",
        "home_sort",
        "menu_featured",
        "filter_sort",
    )
    list_filter = ("is_active", "parent")
    search_fields = ("name_uk", "name_en", "slug")
    ordering = ("sort", "name_uk")


@admin.register(ProductAttributeGroup)
class ProductAttributeGroupAdmin(SlugAdminMixin, GestiaModelAdmin):
    auto_slug = False
    list_display = ("slug", "name_uk")
    search_fields = ("name_uk", "slug")


@admin.register(ProductAttribute)
class ProductAttributeAdmin(SlugAdminMixin, GestiaModelAdmin):
    list_display = ("name_uk", "group", "slug", "sort", "is_filterable")
    list_filter = ("group", "is_filterable")
    search_fields = ("name_uk", "name_en", "slug")


@admin.register(ProductSet)
class ProductSetAdmin(SlugAdminMixin, GestiaModelAdmin):
    list_display = ("name_uk", "slug")
    search_fields = ("name_uk", "name_en", "slug")


@admin.register(CatalogCell)
class CatalogCellAdmin(GestiaModelAdmin):
    list_display = ("product", "surface", "band", "layout", "role", "slot", "sort", "price_uah", "crop")
    list_filter = ("surface", "band", "layout", "role", "slot")
    autocomplete_fields = ("product",)
    ordering = ("band", "sort")


@admin.register(Product)
class ProductAdmin(SlugAdminMixin, GestiaModelAdmin):
    list_display = (
        "name_uk",
        "sku",
        "category",
        "price_uah",
        "price_eur",
        "price_weight",
        "is_popular",
        "stock_status",
        "stock_qty",
        "is_active",
    )
    list_display_links = ("name_uk",)
    list_editable = ("stock_qty",)
    list_filter = ("is_active", "stock_status", "category", "product_set")
    search_fields = ("name_uk", "name_en", "sku", "slug")
    autocomplete_fields = ("category", "product_set")
    filter_horizontal = ("filter_attrs", "related_manual")
    inlines = [ProductImageInline]
    ordering = ("sort", "name_uk")

    def get_fieldsets(self, request, obj=None):
        fieldsets = []
        for title, options in super().get_fieldsets(request, obj):
            fields = []
            pending = None
            for name in options["fields"]:
                if name == "menu_name_uk":
                    pending = name
                    continue
                if pending == "menu_name_uk" and name == "menu_name_en":
                    fields.append(("menu_name_uk", "menu_name_en"))
                    pending = None
                    continue
                if pending:
                    fields.append(pending)
                    pending = None
                fields.append(name)
            if pending:
                fields.append(pending)
            fieldsets.append((title, {**options, "fields": tuple(fields)}))
        return fieldsets
