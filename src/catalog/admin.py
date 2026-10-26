from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.catalog.models import (
    Category,
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductImage,
    ProductSet,
)


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name_uk", "parent", "slug", "is_active", "sort", "home_sort", "menu_featured")
    list_filter = ("is_active", "parent")
    search_fields = ("name_uk", "name_ru", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_uk",)}
    ordering = ("sort", "name_uk")


@admin.register(ProductAttributeGroup)
class ProductAttributeGroupAdmin(ModelAdmin):
    list_display = ("slug", "name_uk")
    search_fields = ("name_uk", "slug")


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = ("name_uk", "group", "slug", "is_filterable")
    list_filter = ("group", "is_filterable")
    search_fields = ("name_uk", "name_ru", "name_en", "slug")


@admin.register(ProductSet)
class ProductSetAdmin(ModelAdmin):
    list_display = ("name_uk", "slug")
    search_fields = ("name_uk", "name_ru", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_uk",)}


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name_uk",
        "sku",
        "category",
        "price_uah",
        "price_eur",
        "price_weight",
        "is_popular",
        "stock_status",
        "is_active",
    )
    list_filter = ("is_active", "stock_status", "category", "product_set")
    search_fields = ("name_uk", "name_ru", "name_en", "sku", "slug")
    prepopulated_fields = {"slug": ("name_uk",)}
    autocomplete_fields = ("category", "product_set")
    filter_horizontal = ("filter_attrs", "related_manual")
    inlines = [ProductImageInline]
    ordering = ("sort", "name_uk")
