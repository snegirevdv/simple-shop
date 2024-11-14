from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for the Product model."""

    list_display = ("name", "slug", "subcategory", "price")
    list_filter = ("subcategory",)
    search_fields = ("name",)
