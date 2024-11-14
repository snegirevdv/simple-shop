from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin interface for CartItem model within Cart."""

    model = CartItem
    extra = 0
    readonly_fields = tuple()
    fields = ("product", "quantity")
    verbose_name = "Cart Item"
    verbose_name_plural = "Cart Items"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for the Cart model."""

    list_display = ("user",)
    search_fields = ("user__username",)
    inlines = (CartItemInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Overrides the default queryset to optimize queries."""
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("cart_items__product")
