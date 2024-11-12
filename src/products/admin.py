from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "subcategory", "price")
    list_filter = ("subcategory",)
    search_fields = ("name",)
