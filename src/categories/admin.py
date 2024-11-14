from django.contrib import admin

from .models import Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for the Category model."""

    list_display = ("name", "slug")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Admin interface for the SubCategory model."""

    list_display = ("name", "slug", "category")
    list_filter = ("category",)
