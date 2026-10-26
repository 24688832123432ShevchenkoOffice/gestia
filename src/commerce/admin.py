from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.commerce.models import Inquiry, Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("sku", "name", "qty", "unit_price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "number",
        "source",
        "customer_name",
        "phone",
        "total",
        "currency",
        "payment_status",
        "created_at",
    )
    list_filter = ("source", "payment_status", "payment_method", "delivery_method", "currency")
    search_fields = ("number", "customer_name", "phone", "email", "items__sku")
    readonly_fields = ("number", "created_at", "total")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"


@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ("created_at", "kind", "name", "phone", "sku", "product_name")
    list_filter = ("kind",)
    search_fields = ("name", "phone", "sku", "product_name", "message")
    readonly_fields = ("created_at",)
